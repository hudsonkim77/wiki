(function () {
  const data = ITSM_DASHBOARD_DATA;

  // ---- 총 자산수 (Hero figure) ----
  document.getElementById('total-assets').textContent = data.totalAssets.toLocaleString();
  document.getElementById('snapshot-date').textContent = data.snapshotDate;

  // ---- 카테고리별 막대바 (카테고리마다 다른 색, 8색 순환) ----
  const chart = document.getElementById('category-bar-chart');
  const maxCount = Math.max(...data.assetsByCategory.map((d) => d.count));
  const CAT_COLORS = 8;

  data.assetsByCategory.forEach((d, i) => {
    const row = document.createElement('div');
    row.className = 'bar-row';

    const displayLabel = d.label || d.category;
    const label = document.createElement('div');
    label.className = 'bar-label';
    label.textContent = displayLabel;
    label.title = displayLabel;

    const track = document.createElement('div');
    track.className = 'bar-track';

    const fill = document.createElement('div');
    fill.className = 'bar-fill';
    fill.style.width = `${(d.count / maxCount) * 100}%`;
    fill.style.background = `var(--cat-${(i % CAT_COLORS) + 1})`;
    track.appendChild(fill);

    const value = document.createElement('div');
    value.className = 'bar-value';
    value.textContent = d.count.toLocaleString();

    row.appendChild(label);
    row.appendChild(track);
    row.appendChild(value);
    chart.appendChild(row);
  });

  // ---- 하단 현황 스코어보드 ----
  const tiles = [
    { label: '변경건수', value: data.scoreboard.changeCount, accent: 'var(--series-2)' },
    { label: '장애건수', value: data.scoreboard.incidentCount, accent: 'var(--series-3)' },
    { label: '구성관리(추가)', value: data.scoreboard.ciAdded, accent: 'var(--series-4)', caption: '이력 미설계 - 0 고정' },
    { label: '구성관리(삭제)', value: data.scoreboard.ciRemoved, accent: 'var(--series-5)', caption: '이력 미설계 - 0 고정' }
  ];

  const scoreboard = document.getElementById('scoreboard');
  tiles.forEach((t) => {
    const tile = document.createElement('div');
    tile.className = 'stat-tile';

    const accent = document.createElement('div');
    accent.className = 'accent';
    accent.style.background = t.accent;

    const value = document.createElement('div');
    value.className = 'value';
    value.textContent = t.value.toLocaleString();

    const label = document.createElement('div');
    label.className = 'label';
    label.textContent = t.label;

    tile.appendChild(accent);
    tile.appendChild(value);
    tile.appendChild(label);

    if (t.caption) {
      const caption = document.createElement('div');
      caption.className = 'caption';
      caption.textContent = t.caption;
      tile.appendChild(caption);
    }

    scoreboard.appendChild(tile);
  });

  // ---- 최근 사항 3건(변경/자산등록/장애) — 행 클릭 시 세부사항 토글 ----
  const recentBox = document.getElementById('recent-items');
  if (recentBox && data.recentItems) {
    data.recentItems.forEach((item) => {
      const wrap = document.createElement('div');
      wrap.className = 'recent-item';

      const row = document.createElement('button');
      row.type = 'button';
      row.className = 'recent-item-row';
      row.setAttribute('aria-expanded', 'false');

      const accent = document.createElement('span');
      accent.className = 'recent-item-badge';
      accent.style.background = `var(--${item.accent})`;
      accent.textContent = item.type;

      const title = document.createElement('span');
      title.className = 'recent-item-title';
      title.textContent = item.title;

      const date = document.createElement('span');
      date.className = 'recent-item-date';
      date.textContent = item.date;

      row.appendChild(accent);
      row.appendChild(title);
      row.appendChild(date);

      const detail = document.createElement('div');
      detail.className = 'recent-item-detail';
      const detailId = document.createElement('div');
      detailId.className = 'recent-item-detail-id';
      detailId.textContent = item.id;
      const detailText = document.createElement('div');
      detailText.textContent = item.detail;
      detail.appendChild(detailId);
      detail.appendChild(detailText);

      row.addEventListener('click', () => {
        const open = wrap.classList.toggle('open');
        row.setAttribute('aria-expanded', open ? 'true' : 'false');
      });

      wrap.appendChild(row);
      wrap.appendChild(detail);
      recentBox.appendChild(wrap);
    });
  }
})();
