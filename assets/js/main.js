document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const navigation = document.querySelector(".nav-links");

  if (toggle && navigation) {
    const closeNavigation = () => {
      toggle.setAttribute("aria-expanded", "false");
      navigation.classList.remove("is-open");
    };

    toggle.addEventListener("click", () => {
      const isOpen = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!isOpen));
      navigation.classList.toggle("is-open", !isOpen);
    });

    navigation.addEventListener("click", (event) => {
      if (event.target.closest("a")) {
        closeNavigation();
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeNavigation();
        toggle.focus();
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 900) closeNavigation();
    });
  }

  const copyButton = document.querySelector("[data-copy-prompt]");
  const promptContent = document.querySelector("[data-prompt-content]");

  if (copyButton && promptContent) {
    copyButton.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(promptContent.innerText.trim());
        copyButton.textContent = "Copied";
        copyButton.classList.add("is-copied");
      } catch (error) {
        copyButton.textContent = "Copy failed";
      }

      window.setTimeout(() => {
        copyButton.textContent = "Copy prompt";
        copyButton.classList.remove("is-copied");
      }, 1800);
    });
  }

  const year = document.querySelector("[data-current-year]");
  if (year) year.textContent = new Date().getFullYear();

  if (window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.querySelectorAll(".bento-card").forEach((card) => {
      card.addEventListener("pointermove", (event) => {
        const bounds = card.getBoundingClientRect();
        card.style.setProperty("--pointer-x", `${event.clientX - bounds.left}px`);
        card.style.setProperty("--pointer-y", `${event.clientY - bounds.top}px`);
      });
    });
  }

  const toneOptions = document.querySelectorAll("[data-tone]");
  const generatedReply = document.querySelector("[data-generated-reply]");
  const toneStatus = document.querySelector("[data-tone-status]");
  const profileScore = document.querySelector(".profile-score");

  if (toneOptions.length && generatedReply && toneStatus && profileScore) {
    const toneProfiles = {
      direct: {
        reply: "Thanks for sending this. I looked through it and the direction feels right. I would keep the opening simple and make the main point clearer.",
        label: "Direct tone",
        score: "92%"
      },
      conversational: {
        reply: "Hey, thanks for sending this over. I went through it and the direction feels right. I would just simplify the opening and bring the main point forward.",
        label: "Conversational tone",
        score: "90%"
      },
      clear: {
        reply: "I reviewed it. The direction is right, but the opening can be simpler and the main point should appear sooner.",
        label: "Clear tone",
        score: "94%"
      },
      personal: {
        reply: "Thanks for sending this. It feels like the right direction to me. I would keep the opening simple so your main point comes through sooner.",
        label: "Personal tone",
        score: "91%"
      }
    };

    toneOptions.forEach((option) => {
      option.addEventListener("click", () => {
        const profile = toneProfiles[option.dataset.tone];
        if (!profile) return;

        toneOptions.forEach((item) => {
          const isSelected = item === option;
          item.classList.toggle("is-active", isSelected);
          item.setAttribute("aria-pressed", String(isSelected));
        });

        generatedReply.textContent = profile.reply;
        toneStatus.textContent = profile.label;
        profileScore.textContent = profile.score;
      });
    });
  }
});
