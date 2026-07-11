// 모든 페이지에서 공유하는 상단 메뉴바 + 하단 푸터 로고.
// 페이지마다 <div id="app-nav"></div> 와 <footer>...</footer>를 두고
// renderNav('home'|'change'|'incident'|'ci')를 호출하면 메뉴바가 그려지고
// (현재 페이지 버튼 활성 표시), 같은 호출이 footer 맨 앞에 로고도 넣어줍니다.
(function () {
  const NAV_ITEMS = [
    { key: 'change', label: '변경관리', href: '변경관리.html' },
    { key: 'incident', label: '장애관리', href: '장애관리.html' },
    { key: 'ci', label: '구성관리', href: '구성관리.html' }
  ];

  const LOGO_MARK_SRC = 'assets/logo-mark.png';
  const LOGO_FULL_SRC = 'assets/logo-full.png';

  window.renderNav = function (activeKey) {
    const root = document.getElementById('app-nav');
    if (root) {
      const nav = document.createElement('nav');
      nav.className = 'navbar';

      const brand = document.createElement('a');
      brand.className = 'brand';
      brand.href = 'index.html';

      const mark = document.createElement('img');
      mark.className = 'brand-mark';
      mark.src = LOGO_MARK_SRC;
      mark.alt = 'AI활성화진흥공단';

      const brandText = document.createElement('span');
      brandText.textContent = 'ITSM 통합관리대시보드';

      brand.appendChild(mark);
      brand.appendChild(brandText);

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
    }

    const footer = document.querySelector('footer');
    if (footer && !footer.querySelector('.footer-logo')) {
      // 기존 footer 안의 링크(<a>)들을 하나의 행으로 묶어 로고 아래에 배치.
      // 페이지마다 footer 마크업을 건드리지 않기 위해 여기서 한 번에 재구성한다.
      const existingLinks = Array.from(footer.children);

      const logo = document.createElement('img');
      logo.className = 'footer-logo';
      logo.src = LOGO_FULL_SRC;
      logo.alt = 'AI활성화진흥공단 · AI Activation & Knowledge Agency';

      const linkRow = document.createElement('div');
      linkRow.className = 'footer-links';
      existingLinks.forEach((el) => linkRow.appendChild(el));

      footer.appendChild(logo);
      footer.appendChild(linkRow);
    }
  };
})();
