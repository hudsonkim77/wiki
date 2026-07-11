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
})();
