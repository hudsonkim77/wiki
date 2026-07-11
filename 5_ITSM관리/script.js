(function () {
  const data = ITSM_DASHBOARD_DATA;

  // ---- 총 자산수 (Hero figure) ----
  document.getElementById('total-assets').textContent = data.totalAssets.toLocaleString();
  document.getElementById('snapshot-date').textContent = data.snapshotDate;

  // ---- 카테고리별 막대바 (Chart.js, 관제형 단일 앰버 그라데이션) ----
  const rootStyle = getComputedStyle(document.documentElement);
  const accentColor = rootStyle.getPropertyValue('--accent').trim();
  const textSecondary = rootStyle.getPropertyValue('--text-secondary').trim();

  const sortedCategories = [...data.assetsByCategory].sort((a, b) => b.count - a.count);
  const canvas = document.getElementById('category-bar-chart');
  canvas.parentElement.style.height = `${28 * sortedCategories.length + 16}px`;

  const ctx = canvas.getContext('2d');
  const barGradient = ctx.createLinearGradient(0, 0, canvas.parentElement.clientWidth || 600, 0);
  barGradient.addColorStop(0, accentColor);
  barGradient.addColorStop(1, '#ffc27a');

  new Chart(canvas, {
    type: 'bar',
    data: {
      labels: sortedCategories.map((d) => d.label || d.category),
      datasets: [{
        data: sortedCategories.map((d) => d.count),
        backgroundColor: barGradient,
        borderRadius: 6,
        barPercentage: 0.7,
      }],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 700, easing: 'easeOutQuart' },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `자산수: ${ctx.formattedValue}건`,
          },
        },
      },
      scales: {
        x: { display: false },
        y: {
          ticks: { color: textSecondary, font: { size: 12 } },
          grid: { display: false },
        },
      },
    },
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
    accent.style.color = t.accent;

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
      accent.style.background = `color-mix(in srgb, var(--${item.accent}) 22%, transparent)`;
      accent.style.color = `var(--${item.accent})`;
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
