// 개인정보처리방침 팝업(모달). 원본 문서: 개인정보처리방침.md (내용 변경 시 이 배열도 함께 갱신)
// 모든 페이지 footer의 <a id="privacy-policy-link"> 클릭을 가로채 팝업으로 띄운다.
(function () {
  const PRIVACY_INTRO =
    "AI활성화진흥공단(이하 '공단')은 「개인정보 보호법」 제30조에 따라 정보주체의 개인정보를 보호하고 이와 관련한 고충을 신속하게 처리하기 위하여 다음과 같이 개인정보 처리방침을 수립·공개합니다.";

  const PRIVACY_SECTIONS = [
    {
      title: "1. 개인정보의 처리 목적",
      body: "공단은 다음의 목적을 위하여 개인정보를 처리합니다. 처리하고 있는 개인정보는 다음의 목적 이외의 용도로는 이용되지 않으며, 이용 목적이 변경되는 경우에는 별도의 동의를 받는 등 필요한 조치를 이행할 예정입니다.",
      list: ["홈페이지 회원 가입 및 관리", "민원 사무 처리 및 사실조사", "시설물 안전 및 화재 예방(CCTV 운영)", "공단 서비스 제공 및 향상"]
    },
    {
      title: "2. 개인정보의 처리 및 보유 기간",
      body: "공단은 법령에 따른 개인정보 보유·이용기간 또는 정보주체로부터 개인정보를 수집 시 동의받은 개인정보 보유·이용기간 내에서 개인정보를 처리·보유합니다.",
      list: ["홈페이지 회원 정보: 회원 탈퇴 시까지", "민원 사무 처리 정보: 민원 처리 종료 후 3년", "영상정보(CCTV): 촬영일로부터 30일 이내"]
    },
    {
      title: "3. 개인정보의 제3자 제공",
      body: "공단은 정보주체의 동의, 법률의 특별한 규정 등 「개인정보 보호법」 제17조 및 제18조에 해당하는 경우에만 개인정보를 제3자에게 제공합니다."
    },
    {
      title: "4. 개인정보처리 위탁",
      body: "공단은 원활한 개인정보 업무처리를 위하여 다음과 같이 개인정보 처리업무를 위탁하고 있습니다.",
      list: ["위탁받는 자: [시스템 운영 및 유지보수 업체명]", "위탁업무: 전산시스템 관리, 보안 점검 등"],
      after: "공단은 위탁계약 체결 시 「개인정보 보호법」 제26조에 따라 위탁업무 수행목적 외 개인정보 처리금지, 기술적·관리적 보호조치 등을 명시하고 감독합니다."
    },
    {
      title: "5. 정보주체와 법정대리인의 권리·의무 및 행사방법",
      body: "정보주체는 공단에 대해 언제든지 개인정보 열람, 정정, 삭제, 처리정지 요구 등의 권리를 행사할 수 있으며, 서면, 전자우편, FAX 등을 통하여 요구할 수 있습니다."
    },
    {
      title: "6. 처리하는 개인정보 항목",
      body: "공단은 다음의 개인정보 항목을 처리하고 있습니다.",
      list: ["필수항목: 성명, 아이디, 비밀번호, 휴대전화번호, 이메일", "자동수집항목: IP주소, 쿠키, 서비스 이용기록"]
    },
    {
      title: "7. 개인정보의 파기",
      body: "공단은 보유기간 경과, 처리 목적 달성 등 불필요하게 된 경우 지체없이 해당 개인정보를 파기합니다. 전자적 파일은 재생 불가능한 기술적 방법을 사용하며, 종이 문서는 분쇄하거나 소각합니다."
    },
    {
      title: "8. 개인정보의 안전성 확보 조치",
      body: "공단은 개인정보 보호를 위해 내부관리계획 수립, 접속기록 보관, 암호화, 해킹 방지 시스템 운영, 접근권한 관리 등의 조치를 취하고 있습니다."
    },
    {
      title: "9. 개인정보 자동 수집 장치의 설치·운영 및 거부",
      body: "공단은 이용자에게 맞춤형 서비스를 제공하기 위해 쿠키(Cookie)를 사용합니다. 이용자는 웹 브라우저 옵션을 통해 쿠키 저장을 거부할 수 있습니다."
    },
    {
      title: "10. 개인정보 보호책임자 지정",
      body: "공단은 개인정보 처리에 관한 업무를 총괄 책임지는 개인정보 보호책임자를 지정하고 있습니다. (연락처: [공단 대표번호])"
    },
    {
      title: "11. 개인정보 열람청구",
      body: "정보주체는 「개인정보 보호법」 제35조에 따른 열람 청구를 할 수 있습니다."
    },
    {
      title: "12. 권익침해 구제방법",
      body: "개인정보침해로 인한 구제를 받기 위하여 개인정보분쟁조정위원회, 한국인터넷진흥원 개인정보침해신고센터 등에 문의할 수 있습니다."
    },
    {
      title: "13. 영상정보처리기기(CCTV) 운영·관리",
      body: "시설안전 및 화재예방을 위해 CCTV를 설치·운영하며, 관리책임자를 지정하여 관리합니다."
    },
    {
      title: "14. 개인정보 처리방침 변경",
      body: "본 개인정보 처리방침은 법령 및 방침에 따라 변경될 수 있으며, 공단 홈페이지를 통해 고지합니다."
    },
    {
      title: "15. 가명정보 처리에 관한 사항",
      body: "공단은 통계작성, 과학적 연구 등을 위하여 필요한 경우 가명정보를 처리하며, 이 경우 법령에 따라 안전하게 관리합니다."
    },
    { title: "16. 개인정보 보호책임자 변경 이력", body: "(필요 시 기재)" },
    { title: "17. 개인정보 보호 전담 부서", body: "(부서명 및 연락처 기재)" },
    { title: "18. 개인정보 보호수준 평가 결과", body: "(공공기관 의무사항 이행 결과 공지)" },
    {
      title: "19. 이용자의 의무",
      body: "이용자는 자신의 개인정보를 최신의 상태로 정확하게 유지해야 하며, 부정확한 정보 입력으로 발생하는 문제의 책임은 이용자에게 있습니다."
    }
  ];

  function buildModal() {
    const overlay = document.createElement("div");
    overlay.className = "modal-overlay";
    overlay.id = "privacy-modal-overlay";

    const panel = document.createElement("div");
    panel.className = "modal-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-modal", "true");
    panel.setAttribute("aria-labelledby", "privacy-modal-title");

    const closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "modal-close";
    closeBtn.setAttribute("aria-label", "닫기");
    closeBtn.textContent = "×";
    closeBtn.addEventListener("click", closeModal);

    const title = document.createElement("h2");
    title.id = "privacy-modal-title";
    title.className = "modal-title";
    title.textContent = "개인정보 처리방침";

    const body = document.createElement("div");
    body.className = "modal-body";

    const intro = document.createElement("p");
    intro.className = "modal-intro";
    intro.textContent = PRIVACY_INTRO;
    body.appendChild(intro);

    PRIVACY_SECTIONS.forEach((section) => {
      const h3 = document.createElement("h3");
      h3.className = "modal-section-title";
      h3.textContent = section.title;
      body.appendChild(h3);

      const p = document.createElement("p");
      p.className = "modal-section-body";
      p.textContent = section.body;
      body.appendChild(p);

      if (section.list) {
        const ul = document.createElement("ul");
        ul.className = "modal-section-list";
        section.list.forEach((item) => {
          const li = document.createElement("li");
          li.textContent = item;
          ul.appendChild(li);
        });
        body.appendChild(ul);
      }

      if (section.after) {
        const pAfter = document.createElement("p");
        pAfter.className = "modal-section-body";
        pAfter.textContent = section.after;
        body.appendChild(pAfter);
      }
    });

    panel.appendChild(closeBtn);
    panel.appendChild(title);
    panel.appendChild(body);
    overlay.appendChild(panel);

    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) closeModal();
    });

    return overlay;
  }

  function openModal() {
    let overlay = document.getElementById("privacy-modal-overlay");
    if (!overlay) {
      overlay = buildModal();
      document.body.appendChild(overlay);
    }
    overlay.classList.add("open");
    document.addEventListener("keydown", onKeydown);
  }

  function closeModal() {
    const overlay = document.getElementById("privacy-modal-overlay");
    if (overlay) overlay.classList.remove("open");
    document.removeEventListener("keydown", onKeydown);
  }

  function onKeydown(e) {
    if (e.key === "Escape") closeModal();
  }

  window.addEventListener("DOMContentLoaded", () => {
    const link = document.getElementById("privacy-policy-link");
    if (!link) return;
    link.addEventListener("click", (e) => {
      e.preventDefault();
      openModal();
    });
  });
})();
