/* BIST Algo Terminal — frontend mantığı */
(() => {
  "use strict";

  const POLL_MS = 2000;
  let pollTimer = null;
  let rows = [];                 // ham sonuç listesi
  let sortKey = "strategy";
  let sortDir = "desc";          // asc | desc
  let regimeFilter = "ALL";

  const $ = (id) => document.getElementById(id);
  const grid = $("grid");

  /* ---------- yardımcılar ---------- */
  const fmt = (v, d = 2) => (v === null || v === undefined ? "—" : Number(v).toFixed(d));

  function rsiColor(rsi) {
    if (rsi === null || rsi === undefined) return { bg: "rgba(107,124,147,.14)", fg: "#6b7c93" };
    if (rsi < 35) return { bg: "rgba(34,197,94,.15)", fg: "#22c55e" };
    if (rsi > 65) return { bg: "rgba(239,68,68,.15)", fg: "#ef4444" };
    return { bg: "rgba(234,179,8,.12)", fg: "#eab308" };
  }

  // strateji öncelik sırası (sıralama için)
  const STRAT_RANK = { KIRILIM_AL: 5, PUSU_AL: 4, TABAN_RISKI: 3, KACIS: 2, IZLE: 0 };
  const REGIME_RANK = { BOGA: 2, YATAY: 1, AYI: 0 };

  /* ---------- KPI ---------- */
  function updateKpis() {
    $("kpiTotal").textContent = rows.length;
    $("kpiBull").textContent = rows.filter((r) => r.regime === "BOGA").length;
    $("kpiBear").textContent = rows.filter((r) => r.regime === "AYI").length;
    $("kpiFlat").textContent = rows.filter((r) => r.regime === "YATAY").length;
    $("kpiAction").textContent = rows.filter((r) => r.is_action).length;
    $("kpiWhale").textContent = rows.filter((r) => r.hacim === "BALINA").length;
  }

  /* ---------- filtre + sıralama ---------- */
  function visibleRows() {
    const q = $("searchInput").value.trim().toUpperCase();
    const actionOnly = $("actionOnly").checked;
    const whaleOnly = $("whaleOnly").checked;

    let out = rows.filter((r) => {
      if (regimeFilter !== "ALL" && r.regime !== regimeFilter) return false;
      if (actionOnly && !r.is_action) return false;
      if (whaleOnly && r.hacim !== "BALINA") return false;
      if (q && !r.symbol.includes(q)) return false;
      return true;
    });

    out.sort((a, b) => {
      let av, bv;
      if (sortKey === "symbol") { av = a.symbol; bv = b.symbol; }
      else if (sortKey === "regime") { av = REGIME_RANK[a.regime]; bv = REGIME_RANK[b.regime]; }
      else if (sortKey === "strategy") { av = STRAT_RANK[a.strategy] ?? 0; bv = STRAT_RANK[b.strategy] ?? 0; }
      else if (sortKey === "hacim") { av = a.volume_zscore ?? -99; bv = b.volume_zscore ?? -99; }
      else { av = a[sortKey] ?? -Infinity; bv = b[sortKey] ?? -Infinity; }

      if (av < bv) return sortDir === "asc" ? -1 : 1;
      if (av > bv) return sortDir === "asc" ? 1 : -1;
      return 0;
    });
    return out;
  }

  function render() {
    const data = visibleRows();
    $("rowCount").textContent = `${data.length} / ${rows.length} hisse`;
    $("emptyState").classList.toggle("hidden", rows.length > 0);

    grid.innerHTML = data
      .map((r) => {
        const rc = rsiColor(r.rsi);
        return `<tr data-sym="${r.symbol}">
          <td class="sym">${r.symbol}</td>
          <td class="num">${fmt(r.fiyat)}</td>
          <td><span class="badge ${r.regime}">${r.regime_label}</span></td>
          <td><span class="badge ${r.hacim}">${r.hacim_label}</span></td>
          <td><span class="strat ${r.strategy}">${r.strategy_label}</span></td>
          <td class="num"><span class="rsi-pill" style="background:${rc.bg};color:${rc.fg}">${fmt(r.rsi, 0)}</span></td>
          <td class="num">${fmt(r.pivot)}</td>
          <td class="num">${fmt(r.stop_loss)}</td>
        </tr>`;
      })
      .join("");

    grid.querySelectorAll("tr").forEach((tr) => {
      tr.addEventListener("click", () => openDrawer(tr.dataset.sym));
    });
  }

  /* ---------- polling / tarama ---------- */
  function applyState(state) {
    rows = state.results || [];
    updateKpis();
    render();

    const { done, total } = state.progress || { done: 0, total: 0 };
    const pct = total ? Math.round((done / total) * 100) : 0;
    $("progressFill").style.width = pct + "%";
    $("progressText").textContent = `${done} / ${total} (%${pct})`;

    if (state.status === "running") {
      $("progressWrap").classList.remove("hidden");
      $("scanBtn").disabled = true;
      $("scanBtn").querySelector(".scan-btn-label").textContent = "⏳ TARANIYOR…";
    } else {
      $("scanBtn").disabled = false;
      $("scanBtn").querySelector(".scan-btn-label").textContent = "↻ YENİDEN TARA";
      if (state.status === "done" || state.status === "error") {
        stopPolling();
        $("progressWrap").classList.add("hidden");
        const ts = state.finished_at ? new Date(state.finished_at * 1000) : new Date();
        $("lastScan").textContent =
          state.status === "error"
            ? "⚠️ Hata: " + (state.error || "bilinmeyen")
            : "Son tarama: " + ts.toLocaleTimeString("tr-TR");
      }
    }
  }

  async function poll() {
    try {
      const res = await fetch("api/results");
      applyState(await res.json());
    } catch (e) { /* sessiz geç */ }
  }

  function startPolling() {
    if (pollTimer) return;
    poll();
    pollTimer = setInterval(poll, POLL_MS);
  }
  function stopPolling() {
    if (pollTimer) { clearInterval(pollTimer); pollTimer = null; }
  }

  async function startScan() {
    $("scanBtn").disabled = true;
    try {
      await fetch("api/scan", { method: "POST" });
      startPolling();
    } catch (e) {
      $("scanBtn").disabled = false;
    }
  }

  /* ---------- detay drawer ---------- */
  async function openDrawer(symbol) {
    $("drawerSym").textContent = symbol;
    $("drawerBody").innerHTML = '<div class="drawer-loading">Yükleniyor…</div>';
    $("drawer").classList.add("open");
    $("drawerOverlay").classList.remove("hidden");

    try {
      const res = await fetch("api/stock/" + encodeURIComponent(symbol));
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        $("drawerBody").innerHTML = `<div class="d-error">⚠️ ${err.error || "Veri alınamadı."}</div>`;
        return;
      }
      renderDetail(await res.json());
    } catch (e) {
      $("drawerBody").innerHTML = '<div class="d-error">⚠️ Bağlantı hatası.</div>';
    }
  }

  function renderDetail(d) {
    const L = d.levels;
    const rc = rsiColor(d.rsi);
    const rejimMap = { BOGA: "🟢 BOĞA", AYI: "🔴 AYI", YATAY: "🟡 YATAY" };
    $("drawerBody").innerHTML = `
      <div class="d-price">${fmt(d.fiyat)} <small>TL</small></div>
      <div style="margin-top:6px"><span class="badge ${d.rejim}">${rejimMap[d.rejim] || d.rejim}</span></div>

      <div class="d-stats">
        <div class="d-stat"><div class="l">RSI</div><div class="v" style="color:${rc.fg}">${fmt(d.rsi, 1)}</div></div>
        <div class="d-stat"><div class="l">Hacim Katı</div><div class="v">${fmt(d.hacim_oran)}x</div></div>
        <div class="d-stat"><div class="l">MA 50</div><div class="v">${fmt(d.ma50)}</div></div>
        <div class="d-stat"><div class="l">MA 200</div><div class="v">${fmt(d.ma200)}</div></div>
      </div>

      <div class="d-section-title">🚨 Kritik Seviyeler</div>
      <div class="levels">
        <div class="level r"><span><span class="tag">DİRENÇ-2</span> <span class="desc">Güçlü satış</span></span><span>${fmt(L.r2)}</span></div>
        <div class="level r"><span><span class="tag">DİRENÇ-1</span> <span class="desc">Ara pivot direnci</span></span><span>${fmt(L.r1)}</span></div>
        <div class="level p"><span><span class="tag">PİVOT</span> <span class="desc">Denge eşiği</span></span><span>${fmt(L.pivot)}</span></div>
        <div class="level s"><span><span class="tag">DESTEK-1</span> <span class="desc">İlk tepki</span></span><span>${fmt(L.s1)}</span></div>
        <div class="level s"><span><span class="tag">DESTEK-2</span> <span class="desc">Majör koruma / stop</span></span><span>${fmt(L.s2)}</span></div>
      </div>

      <div class="d-section-title">📈 Stratejik Yorum</div>
      <div class="yorum">${(d.yorum || []).map((p) => `<p>${p}</p>`).join("")}</div>
    `;
  }

  function closeDrawer() {
    $("drawer").classList.remove("open");
    $("drawerOverlay").classList.add("hidden");
  }

  /* ---------- olay bağlama ---------- */
  function bind() {
    $("scanBtn").addEventListener("click", startScan);
    $("searchInput").addEventListener("input", render);
    $("actionOnly").addEventListener("change", render);
    $("whaleOnly").addEventListener("change", render);
    $("drawerClose").addEventListener("click", closeDrawer);
    $("drawerOverlay").addEventListener("click", closeDrawer);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeDrawer(); });

    $("regimeChips").querySelectorAll(".chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        $("regimeChips").querySelector(".active")?.classList.remove("active");
        chip.classList.add("active");
        regimeFilter = chip.dataset.regime;
        render();
      });
    });

    document.querySelectorAll("th.sortable").forEach((th) => {
      th.addEventListener("click", () => {
        const key = th.dataset.sort;
        if (sortKey === key) sortDir = sortDir === "asc" ? "desc" : "asc";
        else { sortKey = key; sortDir = key === "symbol" ? "asc" : "desc"; }
        document.querySelectorAll("th.sortable").forEach((t) => t.classList.remove("sorted-asc", "sorted-desc"));
        th.classList.add(sortDir === "asc" ? "sorted-asc" : "sorted-desc");
        render();
      });
    });
  }

  bind();
  // Açılışta mevcut durumu çek (önceki tarama varsa göster).
  poll();
})();
