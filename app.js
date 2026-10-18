// StickerBoom — Cross-Platform Mobile Web App & Universal Multi-Social Sticker Engine
// Zero AI Spindle • Instant Local WebP & Transparent PNG Engine for IG, TikTok, iMessage, Telegram, Discord & WhatsApp

(function () {
  const packs = window.STICKERBOOM_PACKS || [];
  const icons = window.STICKERBOOM_ICONS || [];

  // Flatten all 98 stickers with pack reference
  const allStickers = [];
  packs.forEach((pack) => {
    pack.stickers.forEach((s) => {
      allStickers.push({
        ...s,
        packId: pack.id,
        packNumber: pack.number,
        packName: pack.name,
        webpUrl: `assets/stickers/${s.id}.webp`,
        pngUrl: `assets/stickers/${s.id}.png`
      });
    });
  });

  // State
  let activePackId = packs[0]?.id || "pack-1-social-slang";
  let activeStyleFilter = "all"; // 'all' | '3d' | 'sticker'
  let activePlatform = "all"; // 'all' | 'whatsapp' | 'instagram' | 'imessage' | 'telegram' | 'discord'
  let searchQuery = "";
  let selectedSticker = allStickers[0] || null;
  let activeIconId = "icon-1";

  // DOM Elements
  const packRail = document.getElementById("packRail");
  const stickerGrid = document.getElementById("stickerGrid");
  const gridTitle = document.getElementById("gridTitle");
  const gridCount = document.getElementById("gridCount");
  const packBadge = document.getElementById("packBadge");
  const packVol = document.getElementById("packVol");
  const packTitle = document.getElementById("packTitle");
  const packSpecs = document.getElementById("packSpecs");
  const activePackCard = document.getElementById("activePackCard");
  const slangSearchInput = document.getElementById("slangSearchInput");
  const clearSearchBtn = document.getElementById("clearSearchBtn");

  // Live Chat Preview Elements
  const liveChatStickerTitle = document.getElementById("liveChatStickerTitle");
  const liveChatTriggers = document.getElementById("liveChatTriggers");
  const selectedMeaningBox = document.getElementById("selectedMeaningBox");
  const chatSenderName = document.getElementById("chatSenderName");
  const chatIncomingText = document.getElementById("chatIncomingText");
  const chatPreviewStickerImg = document.getElementById("chatPreviewStickerImg");

  // Action Buttons
  const copyStickerClipboardBtn = document.getElementById("copyStickerClipboardBtn");
  const directSendSocialBtn = document.getElementById("directSendSocialBtn");
  const downloadWebpBtn = document.getElementById("downloadWebpBtn");
  const downloadPngBtn = document.getElementById("downloadPngBtn");
  const downloadDiscordBtn = document.getElementById("downloadDiscordBtn");
  const downloadPackBtn = document.getElementById("downloadPackBtn");
  const sharePackBtn = document.getElementById("sharePackBtn");
  const shareAppBtn = document.getElementById("shareAppBtn");

  // Toast
  const toastBanner = document.getElementById("toastBanner");
  let toastTimer = null;

  function showToast(msg) {
    if (!toastBanner) return;
    toastBanner.textContent = msg;
    toastBanner.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toastBanner.classList.remove("show");
    }, 2800);
  }

  // Render Horizontal 8-Pack Rail
  function renderPackRail() {
    packRail.innerHTML = "";
    packs.forEach((pack) => {
      const btn = document.createElement("button");
      btn.className = `pack-pill ${pack.id === activePackId && !searchQuery ? "active" : ""}`;
      btn.textContent = `${pack.shortName} (${pack.stickers.length})`;
      btn.addEventListener("click", () => {
        activePackId = pack.id;
        if (searchQuery) {
          searchQuery = "";
          slangSearchInput.value = "";
          clearSearchBtn.style.display = "none";
        }
        renderPackRail();
        renderActivePackHeader();
        renderStickerGrid();
      });
      packRail.appendChild(btn);
    });
  }

  // Render Active Pack Hero Card
  function renderActivePackHeader() {
    const pack = packs.find((p) => p.id === activePackId) || packs[0];
    if (!pack) return;

    if (searchQuery) {
      activePackCard.style.display = "none";
      return;
    }
    activePackCard.style.display = "block";
    packBadge.textContent = pack.badge;
    packBadge.style.backgroundColor = pack.badgeColor || "#DA1A35";
    packVol.textContent = `Pack ${pack.number} of ${packs.length} • 98 Total`;
    packTitle.textContent = `Pack ${pack.number}: ${pack.name}`;
    packSpecs.textContent = `${pack.stickers.length} Stickers • 512×512 Transparent PNG & WebP (<100KB) • Ready for IG, TikTok, iMessage, Telegram, Discord & WhatsApp`;
  }

  // Filter Stickers
  function getFilteredStickers() {
    const q = searchQuery.trim().toLowerCase();
    let pool = q
      ? allStickers
      : allStickers.filter((s) => s.packId === activePackId);

    if (activeStyleFilter !== "all") {
      pool = pool.filter((s) => s.style === activeStyleFilter);
    }

    if (q) {
      pool = pool.filter(
        (s) =>
          s.name.toLowerCase().includes(q) ||
          (s.variations && s.variations.toLowerCase().includes(q)) ||
          (s.meaning && s.meaning.toLowerCase().includes(q)) ||
          (s.packName && s.packName.toLowerCase().includes(q)) ||
          (s.emojis && s.emojis.some((e) => e.includes(q)))
      );
    }
    return pool;
  }

  // Render 3-Column Sticker Grid
  function renderStickerGrid() {
    const filtered = getFilteredStickers();
    stickerGrid.innerHTML = "";

    if (searchQuery) {
      gridTitle.textContent = `Search Results for "${searchQuery}"`;
    } else {
      gridTitle.textContent = "Tap Sticker to Preview & Send";
    }
    gridCount.textContent = `${filtered.length} shown`;

    if (filtered.length === 0) {
      const empty = document.createElement("div");
      empty.style.gridColumn = "1 / -1";
      empty.style.textAlign = "center";
      empty.style.padding = "28px 12px";
      empty.style.color = "var(--text-muted)";
      empty.innerHTML = `<strong>No matching slang found.</strong><br/><span style="font-size:12px;">Try searching "Steups", "Ent", "Doubles", "Tabanca", or "Soucouyant".</span>`;
      stickerGrid.appendChild(empty);
      return;
    }

    // Ensure selectedSticker is updated if needed
    if (!selectedSticker || !filtered.some((s) => s.id === selectedSticker.id)) {
      updateSelectedSticker(filtered[0], false);
    }

    filtered.forEach((sticker) => {
      const card = document.createElement("article");
      const isSelected = selectedSticker && selectedSticker.id === sticker.id;
      card.className = `sticker-card ${isSelected ? "selected" : ""}`;
      card.setAttribute("role", "button");
      card.setAttribute("tabindex", "0");

      const shortMeaning = sticker.variations
        ? sticker.variations.split("•")[0].trim()
        : sticker.meaning;

      card.innerHTML = `
        <div class="sticker-checkerboard">
          <img src="${sticker.webpUrl}" alt="${sticker.name} Sticker" loading="lazy" onerror="this.src='${sticker.pngUrl}'" />
          <span class="quick-send-badge" title="Select or Quick Send">${isSelected ? "✓" : "+"}</span>
          <span class="style-tag-mini">${sticker.style === "3d" ? "3D" : "SLANG"}</span>
        </div>
        <div class="sticker-meta">
          <div class="sticker-label">${sticker.name}</div>
          <div class="sticker-meaning-short">${shortMeaning}</div>
        </div>
      `;

      card.addEventListener("click", () => {
        updateSelectedSticker(sticker, true);
      });

      stickerGrid.appendChild(card);
    });
  }

  // Update Selected Sticker & Live Social Preview Box
  function updateSelectedSticker(sticker, scrollToPreview) {
    selectedSticker = sticker;

    // Update selected border in grid
    document.querySelectorAll(".sticker-card").forEach((el) => {
      const label = el.querySelector(".sticker-label")?.textContent;
      const isMatch = label === sticker.name;
      el.classList.toggle("selected", isMatch);
      const badge = el.querySelector(".quick-send-badge");
      if (badge) badge.textContent = isMatch ? "✓" : "+";
    });

    liveChatStickerTitle.textContent = `Live Social Preview: "${sticker.name}"`;
    liveChatTriggers.textContent = (sticker.emojis || ["🔥"]).join(" ");
    selectedMeaningBox.innerHTML = `<strong>${sticker.name} (${sticker.variations || "Slang"}):</strong> ${sticker.meaning}`;
    chatSenderName.textContent = sticker.chatSender || "Brethren Crew";
    chatIncomingText.textContent = sticker.chatIncoming || "Wha'appen family! How de vibes looking?";
    chatPreviewStickerImg.src = sticker.webpUrl;
    chatPreviewStickerImg.alt = sticker.name;

    if (scrollToPreview && window.innerWidth < 640) {
      const chatCard = document.getElementById("liveChatSection");
      if (chatCard) {
        chatCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }
  }

  // Convert Image URL to PNG Blob (for Clipboard Copy & Universal Social Share)
  async function fetchStickerPngBlob(sticker, targetSize = 512) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = targetSize;
        canvas.height = targetSize;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, targetSize, targetSize);
        canvas.toBlob((blob) => {
          if (blob) resolve(blob);
          else reject(new Error("Canvas toBlob failed"));
        }, "image/png");
      };
      img.onerror = reject;
      img.src = sticker.pngUrl;
    });
  }

  // Copy Transparent Sticker to Clipboard (Works in IG Stories, iMessage, TikTok, Messenger, X, Discord & WhatsApp)
  async function copyStickerToClipboard(sticker) {
    if (!sticker) return;
    try {
      const size = activePlatform === "discord" ? 128 : 512;
      const pngBlob = await fetchStickerPngBlob(sticker, size);
      if (navigator.clipboard && window.ClipboardItem) {
        await navigator.clipboard.write([
          new ClipboardItem({ "image/png": pngBlob })
        ]);
        showToast(`Copied "${sticker.name}"! Paste in IG Stories, iMessage, TikTok or Discord`);
      } else {
        triggerBlobDownload(pngBlob, `${sticker.id}-${size}px.png`);
        showToast(`Downloaded "${sticker.name}" transparent PNG!`);
      }
    } catch (err) {
      // Fallback to direct download if browser blocks clipboard image write
      const a = document.createElement("a");
      a.href = sticker.pngUrl;
      a.download = `${sticker.id}-stickerboom.png`;
      a.click();
      showToast(`Saved "${sticker.name}" PNG for sharing!`);
    }
  }

  // Native Mobile Share Sheet (navigator.share) for WhatsApp & All Social Apps
  async function directShareSticker(sticker) {
    if (!sticker) return;
    try {
      const useWebp = activePlatform === "whatsapp" || activePlatform === "telegram";
      const fileUrl = useWebp ? sticker.webpUrl : sticker.pngUrl;
      const ext = useWebp ? "webp" : "png";
      const mime = useWebp ? "image/webp" : "image/png";

      const response = await fetch(fileUrl);
      const blob = await response.blob();
      const file = new File([blob], `${sticker.id}-stickerboom.${ext}`, { type: mime });

      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({
          files: [file]
        });
        showToast(`Shared "${sticker.name}"!`);
        return;
      }
    } catch (err) {
      if (err && err.name === "AbortError") return;
    }

    // Fallback: Download exact platform format
    if (activePlatform === "whatsapp" || activePlatform === "telegram") {
      downloadFileUrl(sticker.webpUrl, `${sticker.id}.webp`);
      showToast(`Saved "${sticker.name}" 512×512 WebP (<100KB)!`);
    } else if (activePlatform === "discord") {
      const blob = await fetchStickerPngBlob(sticker, 128);
      triggerBlobDownload(blob, `${sticker.id}-discord-128px.png`);
      showToast(`Saved "${sticker.name}" 128×128 Discord Emoji PNG!`);
    } else {
      downloadFileUrl(sticker.pngUrl, `${sticker.id}.png`);
      showToast(`Saved "${sticker.name}" Transparent PNG for All Socials!`);
    }
  }

  function downloadFileUrl(url, filename) {
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  function triggerBlobDownload(blob, filename) {
    const url = URL.createObjectURL(blob);
    downloadFileUrl(url, filename);
    setTimeout(() => URL.revokeObjectURL(url), 4000);
  }

  // Export Active Pack Metadata + Stickers
  async function exportActivePack() {
    const pack = packs.find((p) => p.id === activePackId) || packs[0];
    if (!pack) return;

    const packManifest = {
      app: "StickerBoom",
      pack_id: pack.id,
      name: pack.name,
      publisher: pack.publisher,
      tray_image_file: pack.trayIcon,
      specs: "512x512 Transparent PNG & WebP (<100KB) + 96x96 PNG Tray Icon",
      social_platforms: ["Instagram", "TikTok", "iMessage", "Telegram", "Messenger", "X", "Discord", "WhatsApp"],
      stickers: pack.stickers.map((s) => ({
        id: s.id,
        name: s.name,
        meaning: s.meaning,
        emojis: s.emojis,
        webp: `assets/stickers/${s.id}.webp`,
        universal_png: `assets/stickers/${s.id}.png`
      }))
    };

    const blob = new Blob([JSON.stringify(packManifest, null, 2)], { type: "application/json" });
    triggerBlobDownload(blob, `${pack.id}-stickerboom-pack.json`);
    if (selectedSticker) {
      downloadFileUrl(selectedSticker.pngUrl, `${selectedSticker.id}.png`);
    }
    showToast(`Exported "${pack.name}" Pack Manifest + Sticker PNG!`);
  }

  // Interactive Full-Screen Group Social Thread (View 2)
  function initInteractiveChatSimulator() {
    const chatLog = document.getElementById("interactiveChatLog");
    const quickTray = document.getElementById("chatQuickTray");
    if (!chatLog || !quickTray) return;

    const starterMessages = [
      {
        sender: "Keisha (St. Augustine)",
        text: "Morning crew! Passing by Doubles man in Curepe right now, slight or heavy pepper?! 🌶️",
        time: "9:15 AM"
      },
      {
        sender: "Devon (San Fernando)",
        text: "Heavy pepper fuh me! And remember tonight is All Fours on de veranda 🃏",
        time: "9:16 AM"
      }
    ];

    chatLog.innerHTML = "";
    starterMessages.forEach((m) => {
      const b = document.createElement("div");
      b.className = "chat-bubble-in";
      b.innerHTML = `
        <div class="chat-sender">${m.sender}</div>
        <div class="chat-text">${m.text}</div>
        <div class="chat-time">${m.time}</div>
      `;
      chatLog.appendChild(b);
    });

    // Populate quick tray with 24 diverse stickers
    quickTray.innerHTML = "";
    allStickers.slice(0, 24).forEach((s) => {
      const btn = document.createElement("button");
      btn.className = "pack-pill";
      btn.style.padding = "4px 10px";
      btn.innerHTML = `<img src="${s.webpUrl}" alt="${s.name}" style="width:28px;height:28px;object-fit:contain;" /> <span>${s.name}</span>`;
      btn.addEventListener("click", () => {
        const out = document.createElement("div");
        out.className = "chat-sticker-out";
        const now = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        out.innerHTML = `
          <img src="${s.webpUrl}" alt="${s.name}" />
          <div class="chat-time">${now} <span class="chat-ticks">Sent</span></div>
        `;
        chatLog.appendChild(out);
        chatLog.scrollTop = chatLog.scrollHeight;
      });
      quickTray.appendChild(btn);
    });
  }

  // Custom Caption Stamp Studio (View 3 — 100% Local Canvas)
  function initCaptionStudio() {
    const canvas = document.getElementById("customStickerCanvas");
    const baseSelect = document.getElementById("studioBaseSelect");
    const topInput = document.getElementById("studioTopTextInput");
    const bottomInput = document.getElementById("studioBottomTextInput");
    const accentSelect = document.getElementById("studioAccentSelect");
    const copyBtn = document.getElementById("studioCopyPngBtn");
    const shareBtn = document.getElementById("studioShareBtn");

    if (!canvas || !baseSelect) return;
    const ctx = canvas.getContext("2d");

    allStickers.forEach((s) => {
      const opt = document.createElement("option");
      opt.value = s.id;
      opt.textContent = `${s.name} (Pack ${s.packNumber})`;
      baseSelect.appendChild(opt);
    });

    function drawRoundedRect(c, x, y, w, h, r) {
      c.beginPath();
      c.moveTo(x + r, y);
      c.arcTo(x + w, y, x + w, y + h, r);
      c.arcTo(x + w, y + h, x, y + h, r);
      c.arcTo(x, y + h, x, y, r);
      c.arcTo(x, y, x + w, y, r);
      c.closePath();
    }

    function renderStudioCanvas() {
      const st = allStickers.find((s) => s.id === baseSelect.value) || allStickers[0];
      const topText = (topInput.value || "").trim().toUpperCase();
      const botText = (bottomInput.value || "").trim().toUpperCase();
      const accent = accentSelect.value || "#F59E0B";

      const img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = () => {
        ctx.clearRect(0, 0, 512, 512);
        // Draw base artwork slightly scaled in center
        ctx.drawImage(img, 26, 28, 460, 420);

        // Top tag pill if provided
        if (topText) {
          ctx.font = "800 22px 'Epilogue', sans-serif";
          const tw = Math.min(460, ctx.measureText(topText).width + 44);
          const tx = (512 - tw) / 2;
          const ty = 14;

          drawRoundedRect(ctx, tx - 4, ty - 4, tw + 8, 46, 23);
          ctx.fillStyle = "#FFFFFF";
          ctx.fill();

          drawRoundedRect(ctx, tx, ty, tw, 38, 19);
          ctx.fillStyle = accent;
          ctx.fill();

          ctx.fillStyle = "#FFFFFF";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(topText, 256, ty + 20);
        }

        // Bottom die-cut slang banner
        if (botText) {
          ctx.font = "800 32px 'Epilogue', sans-serif";
          const bw = Math.min(484, ctx.measureText(botText).width + 52);
          const bx = (512 - bw) / 2;
          const by = 434;

          drawRoundedRect(ctx, bx - 6, by - 6, bw + 12, 68, 32);
          ctx.fillStyle = "#FFFFFF";
          ctx.fill();

          drawRoundedRect(ctx, bx, by, bw, 56, 26);
          ctx.fillStyle = "#121316";
          ctx.fill();
          ctx.lineWidth = 4;
          ctx.strokeStyle = accent;
          ctx.stroke();

          ctx.fillStyle = "#FFFFFF";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(botText, 256, by + 29);
        }
      };
      img.src = st.pngUrl;
    }

    baseSelect.addEventListener("change", renderStudioCanvas);
    topInput.addEventListener("input", renderStudioCanvas);
    bottomInput.addEventListener("input", renderStudioCanvas);
    accentSelect.addEventListener("change", renderStudioCanvas);
    renderStudioCanvas();

    copyBtn?.addEventListener("click", () => {
      canvas.toBlob(async (blob) => {
        if (!blob) return;
        try {
          if (navigator.clipboard && window.ClipboardItem) {
            await navigator.clipboard.write([new ClipboardItem({ "image/png": blob })]);
            showToast("Copied Custom Sticker to Clipboard! Paste in IG, iMessage or TikTok");
            return;
          }
        } catch (_) {}
        triggerBlobDownload(blob, "custom-stickerboom.png");
        showToast("Downloaded Custom 512×512 Transparent PNG!");
      }, "image/png");
    });

    shareBtn?.addEventListener("click", () => {
      canvas.toBlob(async (blob) => {
        if (!blob) return;
        const file = new File([blob], "custom-stickerboom.webp", { type: "image/webp" });
        if (navigator.canShare && navigator.canShare({ files: [file] })) {
          try {
            await navigator.share({
              title: "StickerBoom Custom Sticker",
              files: [file]
            });
            return;
          } catch (_) {}
        }
        triggerBlobDownload(blob, "custom-stickerboom.webp");
        showToast("Saved Custom 512×512 WebP!");
      }, "image/webp", 0.86);
    });
  }

  // PWA & App Icon Switcher + Obsidian Vinyl Peel Splash Controller
  function initIconModal() {
    const modal = document.getElementById("iconModalBackdrop");
    const openBtn = document.getElementById("openIconModalBtn");
    const closeBtn = document.getElementById("closeIconModalBtn");
    const grid = document.getElementById("iconPickerGrid");
    const headerImg = document.getElementById("headerAppIcon");
    const favLink = document.getElementById("faviconLink");
    const touchLink = document.getElementById("appleTouchIconLink");
    const splashEl = document.getElementById("pwaSplashScreen");
    const replaySplashBtn = document.getElementById("replaySplashBtn");

    // Auto-dismiss Splash A smoothly after 1.15s or on tap
    if (splashEl) {
      const dismissSplash = () => splashEl.classList.add("hidden");
      const splashTimer = setTimeout(dismissSplash, 1150);
      splashEl.addEventListener("click", () => {
        clearTimeout(splashTimer);
        dismissSplash();
      });
    }

    if (!modal || !grid) return;

    function renderIcons() {
      grid.innerHTML = "";
      icons.forEach((ic) => {
        const card = document.createElement("div");
        card.className = `icon-option-card ${ic.id === activeIconId ? "active" : ""}`;
        card.innerHTML = `
          <img src="${ic.src}" alt="${ic.name}" />
          <div class="icon-option-name">${ic.name}</div>
        `;
        card.addEventListener("click", () => {
          activeIconId = ic.id;
          if (headerImg) headerImg.src = ic.src;
          if (favLink) favLink.href = ic.src;
          if (touchLink) touchLink.href = ic.src;
          renderIcons();
          showToast(`Active App Icon set to: ${ic.name}`);
        });
        grid.appendChild(card);
      });
    }

    renderIcons();
    openBtn?.addEventListener("click", () => modal.classList.add("open"));
    closeBtn?.addEventListener("click", () => modal.classList.remove("open"));
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.classList.remove("open");
    });

    replaySplashBtn?.addEventListener("click", () => {
      modal.classList.remove("open");
      if (splashEl) {
        splashEl.classList.remove("hidden");
        setTimeout(() => splashEl.classList.add("hidden"), 1500);
      }
    });
  }

  // Event Listeners
  function bindEvents() {
    // Style segmented filter
    document.querySelectorAll(".segment-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".segment-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        activeStyleFilter = btn.getAttribute("data-style-filter") || "all";
        renderStickerGrid();
      });
    });

    // Social platform selector bar
    document.querySelectorAll(".social-pill").forEach((pill) => {
      pill.addEventListener("click", () => {
        document.querySelectorAll(".social-pill").forEach((p) => p.classList.remove("active"));
        pill.classList.add("active");
        activePlatform = pill.getAttribute("data-platform") || "all";
        const platformNames = {
          all: "All Social Apps (Universal PNG & WebP)",
          instagram: "Instagram Stories & TikTok (Transparent PNG Copy)",
          imessage: "iMessage & SMS Sticker Mode",
          telegram: "Telegram & Messenger 512px Mode",
          discord: "Discord & Slack 128×128 Server Emoji Mode",
          whatsapp: "WhatsApp (512×512 WebP <100KB)"
        };
        showToast(`Switched mode: ${platformNames[activePlatform] || "All Socials"}`);
      });
    });

    // Search input
    slangSearchInput?.addEventListener("input", (e) => {
      searchQuery = e.target.value;
      clearSearchBtn.style.display = searchQuery ? "inline-block" : "none";
      renderPackRail();
      renderActivePackHeader();
      renderStickerGrid();
    });

    clearSearchBtn?.addEventListener("click", () => {
      searchQuery = "";
      slangSearchInput.value = "";
      clearSearchBtn.style.display = "none";
      renderPackRail();
      renderActivePackHeader();
      renderStickerGrid();
    });

    // Trending chips
    document.querySelectorAll(".trend-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        const q = chip.getAttribute("data-query") || "";
        searchQuery = q;
        slangSearchInput.value = q;
        clearSearchBtn.style.display = "inline-block";
        renderPackRail();
        renderActivePackHeader();
        renderStickerGrid();
      });
    });

    // Sticker export actions
    copyStickerClipboardBtn?.addEventListener("click", () => copyStickerToClipboard(selectedSticker));
    directSendSocialBtn?.addEventListener("click", () => directShareSticker(selectedSticker));
    downloadWebpBtn?.addEventListener("click", () => {
      if (!selectedSticker) return;
      downloadFileUrl(selectedSticker.webpUrl, `${selectedSticker.id}.webp`);
      showToast(`Downloaded "${selectedSticker.name}" 512×512 WebP (<100KB)!`);
    });
    downloadPngBtn?.addEventListener("click", () => {
      if (!selectedSticker) return;
      downloadFileUrl(selectedSticker.pngUrl, `${selectedSticker.id}.png`);
      showToast(`Downloaded "${selectedSticker.name}" 512×512 Social PNG!`);
    });
    downloadDiscordBtn?.addEventListener("click", async () => {
      if (!selectedSticker) return;
      const blob = await fetchStickerPngBlob(selectedSticker, 128);
      triggerBlobDownload(blob, `${selectedSticker.id}-discord-128px.png`);
      showToast(`Downloaded "${selectedSticker.name}" 128×128 Discord Emoji!`);
    });

    downloadPackBtn?.addEventListener("click", exportActivePack);
    sharePackBtn?.addEventListener("click", () => directShareSticker(selectedSticker));

    shareAppBtn?.addEventListener("click", async () => {
      if (navigator.share) {
        try {
          await navigator.share({
            title: "StickerBoom — Expressive Stickers & Emojis for Every App",
            text: "Check out StickerBoom — 98 expressive emojis & stickers for IG, TikTok, iMessage, Telegram & Discord!",
            url: window.location.href
          });
          return;
        } catch (_) {}
      }
      showToast("StickerBoom link ready to share!");
    });

    // Bottom Navigation Tabs
    document.querySelectorAll(".nav-tab-btn").forEach((tab) => {
      tab.addEventListener("click", () => {
        const targetId = tab.getAttribute("data-nav-target");
        document.querySelectorAll(".nav-tab-btn").forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");

        document.querySelectorAll(".view-panel").forEach((panel) => {
          panel.classList.toggle("active", panel.id === targetId);
        });
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    });
  }

  // Initialize App
  renderPackRail();
  renderActivePackHeader();
  renderStickerGrid();
  if (selectedSticker) updateSelectedSticker(selectedSticker, false);
  initInteractiveChatSimulator();
  initCaptionStudio();
  initIconModal();
  bindEvents();
})();
