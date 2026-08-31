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
});
