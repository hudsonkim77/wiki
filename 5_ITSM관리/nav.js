// 모든 페이지에서 공유하는 상단 메뉴바.
// 페이지마다 <div id="app-nav"></div> 를 두고 renderNav('home'|'change'|'incident'|'ci')를 호출하면
// 동일한 메뉴바가 그려지고, 현재 페이지에 해당하는 버튼이 활성 표시됩니다.
(function () {
  const NAV_ITEMS = [
    { key: 'change', label: '변경관리', href: '변경관리.html' },
    { key: 'incident', label: '장애관리', href: '장애관리.html' },
    { key: 'ci', label: '구성관리', href: '구성관리.html' }
  ];

  window.renderNav = function (activeKey) {
    const root = document.getElementById('app-nav');
    if (!root) return;

    const nav = document.createElement('nav');
    nav.className = 'navbar';

    const brand = document.createElement('a');
    brand.className = 'brand';
    brand.href = 'index.html';
    brand.textContent = 'ITSM 통합관리대시보드';

    const buttons = document.createElement('div');
    buttons.className = 'nav-buttons';

    NAV_ITEMS.forEach((item) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = item.label;
      if (item.key === activeKey) btn.classList.add('active');
      btn.addEventListener('click', () => {
        window.location.href = item.href;
      });
      buttons.appendChild(btn);
    });

    nav.appendChild(brand);
    nav.appendChild(buttons);
    root.appendChild(nav);
  };
})();
