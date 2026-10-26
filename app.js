// PeelOff — Cross-Platform Mobile Web App & Universal Multi-Social Sticker Engine
// 100% Real Local PNG, WebP & .ZIP Pack Engine for IG, TikTok, iMessage, Telegram, Discord & WhatsApp

(function () {
  const packs = window.STICKERBOOM_PACKS || [];
  const icons = window.STICKERBOOM_ICONS || [];
  const triniSlangList = window.STICKERBOOM_TRINI_SLANG || [];

  // Flatten all 98 stickers with pack reference + Animated WebP & GIF URLs
  const allStickers = [];
  packs.forEach((pack) => {
    pack.stickers.forEach((s) => {
      allStickers.push({
        ...s,
        packId: pack.id,
        packNumber: pack.number,
        packName: pack.name,
        webpUrl: `assets/stickers/${s.id}.webp?v=4`,
        pngUrl: `assets/stickers/${s.id}.png?v=4`,
        animWebpUrl: `assets/animated/${s.id}.webp?v=4`,
        animGifUrl: `assets/animated/${s.id}.gif?v=4`
      });
    });
  });

  // Enrich all 88 Trini Slang items with Animated WebP & GIF URLs
  triniSlangList.forEach((item) => {
    item.animWebpUrl = `assets/animated/${item.id}.webp?v=4`;
    item.animGifUrl = `assets/animated/${item.id}.gif?v=4`;
  });

  // State
  let activePackId = packs[0]?.id || "pack-1-social-slang";
  let activeStyleFilter = "all"; // 'all' | '3d' | 'sticker'
  let activePlatform = "all"; // 'all' | 'instagram' | 'imessage' | 'telegram' | 'discord' | 'whatsapp'
  let isAnimatedMode = true; // Live animated WebP/GIF mode ON by default
  let searchQuery = "";
  let selectedSticker = allStickers[0] || null;
  let activeIconId = "icon-1";
  let refreshSlangViewFn = null;

  // DOM Elements
  const packRail = document.getElementById("packRail");
  const stickerGrid = document.getElementById("stickerGrid");
  const gridTitle = document.getElementById("gridTitle");
  const gridCount = document.getElementById("gridCount");
  const packBadge = document.getElementById("packBadge");
  const packVol = document.getElementById("packVol");
  const packTitle = document.getElementById("packTitle");
  const activePackCard = document.getElementById("activePackCard");
  const slangSearchInput = document.getElementById("slangSearchInput");
  const clearSearchBtn = document.getElementById("clearSearchBtn");
  const downloadPackBtnLabel = document.getElementById("downloadPackBtnLabel");
  const toggleAnimatedBtn = document.getElementById("toggleAnimatedBtn");
  const toggleAnimatedLabel = document.getElementById("toggleAnimatedLabel");

  // Selected Sticker Inspector Elements
  const liveChatStickerTitle = document.getElementById("liveChatStickerTitle");
  const selectedStickerFormatBadge = document.getElementById("selectedStickerFormatBadge");
  const chatPreviewStickerImg = document.getElementById("chatPreviewStickerImg");

  // Action Buttons
  const copyStickerClipboardBtn = document.getElementById("copyStickerClipboardBtn");
  const directSendSocialBtn = document.getElementById("directSendSocialBtn");
  const downloadAnimGifBtn = document.getElementById("downloadAnimGifBtn");
  const downloadAnimWebpBtn = document.getElementById("downloadAnimWebpBtn");
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
    }, 2600);
  }

  const SVG_CHECK = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`;
  const SVG_PLUS = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>`;
  const SVG_EYE = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>`;

  // Render Horizontal 8-Pack Rail
  function renderPackRail() {
    packRail.innerHTML = "";
    packs.forEach((pack) => {
      const btn = document.createElement("button");
      btn.className = `pack-pill ${pack.id === activePackId && !searchQuery ? "active" : ""}`;
      const cleanShort = pack.shortName.replace(/^[^\w]+/, "").trim();
      btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg><span>${cleanShort} (${pack.stickers.length})</span>`;
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
    packBadge.style.backgroundColor = pack.badgeColor || "#E03A26";
    packVol.textContent = `Pack ${pack.number} of ${packs.length} • ${pack.stickers.length} Stickers`;
    packTitle.textContent = `Pack ${pack.number}: ${pack.name}`;
    if (downloadPackBtnLabel) {
      downloadPackBtnLabel.textContent = `Download Pack ${pack.number} (.ZIP — ${pack.stickers.length} Stickers)`;
    }
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
          (s.packName && s.packName.toLowerCase().includes(q))
      );
    }
    return pool;
  }

  // Render 3-Column Sticker Grid (Clean: Only Artwork + Sticker Title, No Description Text)
  function renderStickerGrid() {
    const filtered = getFilteredStickers();
    stickerGrid.innerHTML = "";

    if (gridTitle) {
      gridTitle.textContent = searchQuery
        ? `Results for "${searchQuery}"`
        : "Tap Any Sticker to Copy or Send";
    }
    if (gridCount) {
      gridCount.textContent = `${filtered.length} stickers`;
    }

    if (filtered.length === 0) {
      const empty = document.createElement("div");
      empty.style.gridColumn = "1 / -1";
      empty.style.textAlign = "center";
      empty.style.padding = "28px 12px";
      empty.style.color = "var(--text-muted)";
      empty.innerHTML = `<strong>No matching stickers found.</strong><br/><span style="font-size:12px;">Try searching "Steups", "Ent", "Doubles", "Tabanca", or "Soucouyant".</span>`;
      stickerGrid.appendChild(empty);
      return;
    }

    if (!selectedSticker || !filtered.some((s) => s.id === selectedSticker.id)) {
      updateSelectedSticker(filtered[0], false);
    }

    filtered.forEach((sticker) => {
      const card = document.createElement("article");
      const isSelected = selectedSticker && selectedSticker.id === sticker.id;
      card.className = `sticker-card ${isSelected ? "selected" : ""}`;
      card.setAttribute("role", "button");
      card.setAttribute("tabindex", "0");

      const displaySrc = isAnimatedMode ? sticker.animWebpUrl : sticker.webpUrl;
      card.innerHTML = `
        <div class="sticker-checkerboard">
          <img src="${displaySrc}" alt="${sticker.name}" loading="lazy" onerror="this.src='${sticker.webpUrl}'" />
          <span class="quick-send-badge" title="Selected">${isSelected ? SVG_CHECK : SVG_PLUS}</span>
          <span class="style-tag-mini">${isAnimatedMode ? "⚡ ANIM" : sticker.style === "3d" ? "3D" : "SLANG"}</span>
        </div>
        <div class="sticker-meta">
          <div class="sticker-label">${sticker.name}</div>
        </div>
      `;

      card.addEventListener("click", () => {
        updateSelectedSticker(sticker, true);
      });

      stickerGrid.appendChild(card);
    });
  }

  // Update Selected Sticker Inspector (No Description Text or Fake Chat)
  function updateSelectedSticker(sticker, scrollToPreview) {
    selectedSticker = sticker;

    document.querySelectorAll(".sticker-card").forEach((el) => {
      const label = el.querySelector(".sticker-label")?.textContent;
      const isMatch = label === sticker.name;
      el.classList.toggle("selected", isMatch);
      const badge = el.querySelector(".quick-send-badge");
      if (badge) badge.innerHTML = isMatch ? SVG_CHECK : SVG_PLUS;
    });

    if (liveChatStickerTitle) {
      liveChatStickerTitle.textContent = sticker.name;
    }
    if (selectedStickerFormatBadge) {
      const styleLabel = sticker.style === "3d" ? "3D Emoji" : "Die-Cut Slang Sticker";
      selectedStickerFormatBadge.textContent = isAnimatedMode
        ? `${styleLabel} • Animated GIF & WebP + PNG`
        : `${styleLabel} • 512×512 PNG & WebP`;
    }
    if (chatPreviewStickerImg) {
      chatPreviewStickerImg.src = isAnimatedMode ? sticker.animWebpUrl : sticker.webpUrl;
      chatPreviewStickerImg.alt = sticker.name;
    }

    if (scrollToPreview && window.innerWidth < 640) {
      const inspectorCard = document.getElementById("liveChatSection");
      if (inspectorCard) {
        inspectorCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }
  }

  // Convert Image URL to PNG Blob (for Clipboard Copy & Discord Resize)
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

  // Copy Transparent Sticker to Clipboard (or Share Animated GIF when Animated Mode is ON)
  async function copyStickerToClipboard(sticker) {
    if (!sticker) return;
    if (isAnimatedMode) {
      showToast(`Opening Share Sheet for Animated GIF (Clipboards only support static PNG)`);
      await directShareSticker(sticker);
      return;
    }
    try {
      const size = activePlatform === "discord" ? 128 : 512;
      const pngBlob = await fetchStickerPngBlob(sticker, size);
      if (navigator.clipboard && window.ClipboardItem) {
        await navigator.clipboard.write([
          new ClipboardItem({ "image/png": pngBlob })
        ]);
        showToast(`Copied "${sticker.name}" sticker! Paste into any app`);
      } else {
        triggerBlobDownload(pngBlob, `${sticker.id}-${size}px.png`);
        showToast(`Downloaded "${sticker.name}" transparent PNG!`);
      }
    } catch (err) {
      downloadFileUrl(sticker.pngUrl, `${sticker.id}.png`);
      showToast(`Saved "${sticker.name}" PNG!`);
    }
  }

  // Native Mobile Share Sheet (Always uses 2.16s Looping GIF in Animated Mode so WhatsApp/IG/iMessage animate it!)
  async function directShareSticker(sticker) {
    if (!sticker) return;
    try {
      const useWebp = activePlatform === "whatsapp" || activePlatform === "telegram";
      let fileUrl = sticker.pngUrl;
      let ext = "png";
      let mime = "image/png";

      if (isAnimatedMode) {
        // IMPORTANT: Mobile OS Share Sheets (especially WhatsApp) flatten shared .webp files to static images.
        // Sharing a 2.16-second looping .gif makes WhatsApp, iMessage, Instagram, Discord & Telegram play the animation!
        fileUrl = sticker.animGifUrl;
        ext = "gif";
        mime = "image/gif";
      } else if (useWebp) {
        fileUrl = sticker.webpUrl;
        ext = "webp";
        mime = "image/webp";
      }

      const response = await fetch(fileUrl);
      const blob = await response.blob();
      const file = new File([blob], `${sticker.id}.${ext}`, { type: mime });

      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({
          files: [file]
        });
        showToast(`Sent "${sticker.name}" (${ext.toUpperCase()})!`);
        return;
      }
    } catch (err) {
      if (err && err.name === "AbortError") return;
    }

    // Fallback: Download exact platform image format
    if (isAnimatedMode) {
      downloadFileUrl(sticker.animGifUrl, `${sticker.id}-animated.gif`);
      showToast(`Saved "${sticker.name}" Animated GIF!`);
    } else if (activePlatform === "whatsapp" || activePlatform === "telegram") {
      downloadFileUrl(sticker.webpUrl, `${sticker.id}.webp`);
      showToast(`Saved "${sticker.name}" 512×512 WebP!`);
    } else if (activePlatform === "discord") {
      const blob = await fetchStickerPngBlob(sticker, 128);
      triggerBlobDownload(blob, `${sticker.id}-discord-128px.png`);
      showToast(`Saved "${sticker.name}" 128×128 Discord PNG!`);
    } else {
      downloadFileUrl(sticker.pngUrl, `${sticker.id}.png`);
      showToast(`Saved "${sticker.name}" 512×512 Transparent PNG!`);
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

  // Download Real .ZIP Archive Containing All Stickers in the Active Pack
  function exportActivePack() {
    const pack = packs.find((p) => p.id === activePackId) || packs[0];
    if (!pack) return;
    const zipUrl = `assets/packs/${pack.id}.zip`;
    downloadFileUrl(zipUrl, `${pack.id}-stickers.zip`);
    showToast(`Downloading "${pack.name}" (${pack.stickers.length} Stickers .ZIP)`);
  }

  // Custom Caption Stamp Studio (View 2 — 100% Local HTML5 Canvas)
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

    triniSlangList.forEach((s) => {
      const opt = document.createElement("option");
      opt.value = s.id;
      opt.textContent = `🗣️ ${s.name} (Trini Slang #${s.num})`;
      baseSelect.appendChild(opt);
    });

    const combinedStudioPool = [...allStickers, ...triniSlangList];

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
      const st = combinedStudioPool.find((s) => s.id === baseSelect.value) || combinedStudioPool[0];
      const topText = (topInput.value || "").trim().toUpperCase();
      const botText = (bottomInput.value || "").trim().toUpperCase();
      const accent = accentSelect.value || "#F59E0B";

      const img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = () => {
        ctx.clearRect(0, 0, 512, 512);
        ctx.drawImage(img, 26, 28, 460, 420);

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
            showToast("Copied Custom Sticker to Clipboard!");
            return;
          }
        } catch (_) {}
        triggerBlobDownload(blob, "custom-peeloff.png");
        showToast("Downloaded Custom 512×512 Transparent PNG!");
      }, "image/png");
    });

    shareBtn?.addEventListener("click", () => {
      canvas.toBlob(async (blob) => {
        if (!blob) return;
        const file = new File([blob], "custom-peeloff.png", { type: "image/png" });
        if (navigator.canShare && navigator.canShare({ files: [file] })) {
          try {
            await navigator.share({
              files: [file]
            });
            return;
          } catch (_) {}
        }
        triggerBlobDownload(blob, "custom-peeloff.png");
        showToast("Saved Custom 512×512 PNG!");
      }, "image/png");
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

  // Universal Trini Slang 88-Item Pictorial Controller (View 2)
  function initTriniSlangSection() {
    const catRail = document.getElementById("slangCategoryRail");
    const grid = document.getElementById("triniSlangGrid");
    const gridTitleEl = document.getElementById("slangGridTitle");
    const gridCountEl = document.getElementById("slangGridCount");
    const catBadgeEl = document.getElementById("slangCategoryCountBadge");
    const sectionTitleEl = document.getElementById("slangSectionTitle");
    const searchInput = document.getElementById("triniSlangSearchInput");
    const clearBtn = document.getElementById("clearTriniSlangSearchBtn");
    const toggleMeaningBtn = document.getElementById("toggleSlangMeaningBtn");
    const downloadZipBtn = document.getElementById("downloadAllSlangZipBtn");

    // Inspector Elements
    const previewImg = document.getElementById("slangPreviewImg");
    const metaTag = document.getElementById("slangInspectorMetaTag");
    const titleEl = document.getElementById("slangInspectorTitle");
    const meaningEl = document.getElementById("slangInspectorMeaning");
    const visualEl = document.getElementById("slangInspectorVisual");

    // Inspector Export Buttons
    const copyBtn = document.getElementById("copySlangClipboardBtn");
    const sendBtn = document.getElementById("directSendSlangBtn");
    const animGifBtn = document.getElementById("downloadSlangAnimGifBtn");
    const animWebpBtn = document.getElementById("downloadSlangAnimWebpBtn");
    const pngBtn = document.getElementById("downloadSlangPngBtn");
    const discordBtn = document.getElementById("downloadSlangDiscordBtn");

    if (!grid || !catRail || triniSlangList.length === 0) return;

    const CATEGORIES = [
      "All",
      "Greetings & Links",
      "Co-Signs & Facts",
      "Disbelief & Comedy",
      "Attitude & Shade",
      "People & Drama",
      "Vibes, Belly & Money"
    ];

    let activeSlangCat = "All";
    let slangQuery = "";
    let showSlangMeanings = true;
    let selectedSlang = triniSlangList.find((i) => i.slug === "red-flag") || triniSlangList[0];

    function renderSlangCategoryRail() {
      catRail.innerHTML = "";
      CATEGORIES.forEach((cat) => {
        const count =
          cat === "All"
            ? triniSlangList.length
            : triniSlangList.filter((item) => item.category === cat).length;
        const btn = document.createElement("button");
        btn.className = `pack-pill ${cat === activeSlangCat && !slangQuery ? "active" : ""}`;
        btn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg><span>${cat} (${count})</span>`;
        btn.addEventListener("click", () => {
          activeSlangCat = cat;
          if (slangQuery) {
            slangQuery = "";
            if (searchInput) searchInput.value = "";
            if (clearBtn) clearBtn.style.display = "none";
          }
          renderSlangCategoryRail();
          renderSlangGrid();
        });
        catRail.appendChild(btn);
      });
    }

    function updateSelectedSlang(item, scrollToInspector) {
      selectedSlang = item;

      grid.querySelectorAll(".sticker-card").forEach((card) => {
        const isMatch = card.getAttribute("data-slang-id") === item.id;
        card.classList.toggle("selected", isMatch);
        const badge = card.querySelector(".quick-send-badge");
        if (badge) badge.innerHTML = isMatch ? SVG_CHECK : SVG_PLUS;
      });

      if (previewImg) {
        previewImg.src = isAnimatedMode ? item.animWebpUrl : item.webpUrl;
        previewImg.alt = item.name;
      }
      if (metaTag) {
        metaTag.textContent = `ROW #${item.num} • ${item.category.toUpperCase()}`;
      }
      if (titleEl) {
        titleEl.textContent = item.name;
      }
      if (meaningEl) {
        meaningEl.textContent = `Meaning: "${item.meaning}"`;
      }
      if (visualEl) {
        visualEl.textContent = `🎯 ${item.visual}`;
      }

      if (scrollToInspector && window.innerWidth < 640) {
        const inspector = document.getElementById("slangInspectorSection");
        if (inspector) {
          inspector.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
      }
    }

    function renderSlangGrid() {
      const q = slangQuery.trim().toLowerCase();
      const filtered = triniSlangList.filter((item) => {
        if (!q && activeSlangCat !== "All" && item.category !== activeSlangCat) {
          return false;
        }
        if (q) {
          return (
            item.name.toLowerCase().includes(q) ||
            item.meaning.toLowerCase().includes(q) ||
            item.visual.toLowerCase().includes(q) ||
            item.category.toLowerCase().includes(q) ||
            `#${item.num}` === q
          );
        }
        return true;
      });

      grid.innerHTML = "";
      if (gridCountEl) {
        gridCountEl.textContent = `${filtered.length} icons`;
      }
      if (catBadgeEl) {
        catBadgeEl.textContent = `${filtered.length} of ${triniSlangList.length} Slang Icons`;
      }
      if (sectionTitleEl) {
        sectionTitleEl.textContent =
          activeSlangCat === "All"
            ? "Trini Slang Pictorial Hub (All 88 Items)"
            : `Trini Slang: ${activeSlangCat}`;
      }
      if (gridTitleEl) {
        gridTitleEl.textContent = q
          ? `Results for "${slangQuery}"`
          : "Tap Any Icon to Copy or Send";
      }

      if (filtered.length === 0) {
        const empty = document.createElement("div");
        empty.style.gridColumn = "1 / -1";
        empty.style.textAlign = "center";
        empty.style.padding = "28px 12px";
        empty.style.color = "var(--text-muted)";
        empty.innerHTML = `<strong>No matching Trini Slang icon found.</strong><br/><span style="font-size:12px;">Try searching "Red flag", "Cap", "Take a set", "Eagle", or "Vex".</span>`;
        grid.appendChild(empty);
        return;
      }

      if (!selectedSlang || !filtered.some((i) => i.id === selectedSlang.id)) {
        updateSelectedSlang(filtered[0], false);
      }

      filtered.forEach((item) => {
        const card = document.createElement("article");
        const isSelected = selectedSlang && selectedSlang.id === item.id;
        card.className = `sticker-card ${isSelected ? "selected" : ""}`;
        card.setAttribute("data-slang-id", item.id);
        card.setAttribute("role", "button");
        card.setAttribute("tabindex", "0");

        const slangDisplaySrc = isAnimatedMode ? item.animWebpUrl : item.webpUrl;
        card.innerHTML = `
          <div class="sticker-checkerboard">
            <img src="${slangDisplaySrc}" alt="${item.name}" loading="lazy" onerror="this.src='${item.webpUrl}'" />
            <span class="quick-send-badge" title="Selected">${isSelected ? SVG_CHECK : SVG_PLUS}</span>
            <span class="style-tag-mini">${isAnimatedMode ? "⚡ #" + item.num : "#" + item.num}</span>
          </div>
          <div class="sticker-meta">
            <div class="sticker-label">${item.name}</div>
            ${
              showSlangMeanings
                ? `<div class="sticker-meaning-short" title="${item.meaning}">${item.meaning}</div>`
                : ""
            }
          </div>
        `;

        card.addEventListener("click", () => updateSelectedSlang(item, true));
        grid.appendChild(card);
      });
    }

    searchInput?.addEventListener("input", (e) => {
      slangQuery = e.target.value;
      if (clearBtn) clearBtn.style.display = slangQuery ? "inline-block" : "none";
      renderSlangCategoryRail();
      renderSlangGrid();
    });

    clearBtn?.addEventListener("click", () => {
      slangQuery = "";
      if (searchInput) searchInput.value = "";
      clearBtn.style.display = "none";
      renderSlangCategoryRail();
      renderSlangGrid();
    });

    document.querySelectorAll(".slang-quick-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        const q = chip.getAttribute("data-slang-query") || "";
        slangQuery = q;
        if (searchInput) searchInput.value = q;
        if (clearBtn) clearBtn.style.display = "inline-block";
        renderSlangCategoryRail();
        renderSlangGrid();
      });
    });

    toggleMeaningBtn?.addEventListener("click", () => {
      showSlangMeanings = !showSlangMeanings;
      toggleMeaningBtn.innerHTML = `${SVG_EYE}<span>Meanings: ${showSlangMeanings ? "ON" : "OFF"}</span>`;
      renderSlangGrid();
    });

    downloadZipBtn?.addEventListener("click", () => {
      downloadFileUrl("assets/packs/trini-slang-all-88.zip", "trini-slang-all-88-stickers.zip");
      showToast("Downloading All 88 Trini Slang 3D Icons (.ZIP)!");
    });

    copyBtn?.addEventListener("click", () => copyStickerToClipboard(selectedSlang));
    sendBtn?.addEventListener("click", () => directShareSticker(selectedSlang));
    animGifBtn?.addEventListener("click", () => {
      if (!selectedSlang) return;
      downloadFileUrl(selectedSlang.animGifUrl, `${selectedSlang.id}-animated.gif`);
      showToast(`Downloaded "${selectedSlang.name}" Animated GIF!`);
    });
    animWebpBtn?.addEventListener("click", () => {
      if (!selectedSlang) return;
      downloadFileUrl(selectedSlang.animWebpUrl, `${selectedSlang.id}-animated.webp`);
      showToast(`Downloaded "${selectedSlang.name}" Animated WebP!`);
    });
    pngBtn?.addEventListener("click", () => {
      if (!selectedSlang) return;
      downloadFileUrl(selectedSlang.pngUrl, `${selectedSlang.id}.png`);
      showToast(`Downloaded "${selectedSlang.name}" 512×512 PNG!`);
    });
    discordBtn?.addEventListener("click", async () => {
      if (!selectedSlang) return;
      if (isAnimatedMode) {
        downloadFileUrl(selectedSlang.animGifUrl, `${selectedSlang.id}-discord.gif`);
        showToast(`Downloaded "${selectedSlang.name}" Animated Discord GIF!`);
        return;
      }
      const blob = await fetchStickerPngBlob(selectedSlang, 128);
      triggerBlobDownload(blob, `${selectedSlang.id}-discord-128px.png`);
      showToast(`Downloaded "${selectedSlang.name}" 128×128 Discord PNG!`);
    });

    refreshSlangViewFn = () => {
      renderSlangGrid();
      if (selectedSlang) updateSelectedSlang(selectedSlang, false);
    };

    renderSlangCategoryRail();
    renderSlangGrid();
    if (selectedSlang) updateSelectedSlang(selectedSlang, false);
  }

  // Event Listeners
  function bindEvents() {
    function switchTriniSubView(targetViewId) {
      document.querySelectorAll(".trini-subtab-btn").forEach((b) => {
        const isMatch = b.getAttribute("data-trini-subview") === targetViewId;
        b.classList.toggle("active", isMatch);
        b.setAttribute("aria-selected", isMatch ? "true" : "false");
      });

      document.querySelectorAll(".nav-tab-btn").forEach((t) => {
        t.classList.toggle("active", t.getAttribute("data-nav-target") === targetViewId);
      });

      document.querySelectorAll(".view-panel").forEach((panel) => {
        panel.classList.toggle("active", panel.id === targetViewId);
      });
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    document.querySelectorAll(".trini-subtab-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetViewId = btn.getAttribute("data-trini-subview") || "view-packs";
        switchTriniSubView(targetViewId);
      });
    });

    document.getElementById("triniHubFlagBadge")?.addEventListener("click", () => {
      const currentActive = document.querySelector(".trini-subtab-btn.active");
      const targetViewId = currentActive?.getAttribute("data-trini-subview") || "view-packs";
      switchTriniSubView(targetViewId);
    });

    document.querySelectorAll(".segment-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".segment-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");

        switchTriniSubView("view-packs");
        activeStyleFilter = btn.getAttribute("data-style-filter") || "all";
        renderStickerGrid();
      });
    });

    document.querySelectorAll(".social-pill").forEach((pill) => {
      pill.addEventListener("click", () => {
        document.querySelectorAll(".social-pill").forEach((p) => p.classList.remove("active"));
        pill.classList.add("active");
        activePlatform = pill.getAttribute("data-platform") || "all";
        const platformNames = {
          all: "All Social Apps (512×512 PNG)",
          instagram: "Instagram Stories & TikTok (PNG Copy)",
          imessage: "iMessage & SMS Sticker Mode",
          telegram: "Telegram & Messenger 512px Mode",
          discord: "Discord & Slack 128×128 Emoji Mode",
          whatsapp: "WhatsApp (512×512 WebP <100KB)"
        };
        showToast(`Format: ${platformNames[activePlatform] || "All Socials"}`);
      });
    });

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

    copyStickerClipboardBtn?.addEventListener("click", () => copyStickerToClipboard(selectedSticker));
    directSendSocialBtn?.addEventListener("click", () => directShareSticker(selectedSticker));
    downloadAnimGifBtn?.addEventListener("click", () => {
      if (!selectedSticker) return;
      downloadFileUrl(selectedSticker.animGifUrl, `${selectedSticker.id}-animated.gif`);
      showToast(`Downloaded "${selectedSticker.name}" Animated GIF!`);
    });
    downloadAnimWebpBtn?.addEventListener("click", () => {
      if (!selectedSticker) return;
      downloadFileUrl(selectedSticker.animWebpUrl, `${selectedSticker.id}-animated.webp`);
      showToast(`Downloaded "${selectedSticker.name}" Animated WebP!`);
    });
    downloadPngBtn?.addEventListener("click", () => {
      if (!selectedSticker) return;
      downloadFileUrl(selectedSticker.pngUrl, `${selectedSticker.id}.png`);
      showToast(`Downloaded "${selectedSticker.name}" 512×512 PNG!`);
    });
    downloadDiscordBtn?.addEventListener("click", async () => {
      if (!selectedSticker) return;
      if (isAnimatedMode) {
        downloadFileUrl(selectedSticker.animGifUrl, `${selectedSticker.id}-discord.gif`);
        showToast(`Downloaded "${selectedSticker.name}" Animated Discord GIF!`);
        return;
      }
      const blob = await fetchStickerPngBlob(selectedSticker, 128);
      triggerBlobDownload(blob, `${selectedSticker.id}-discord-128px.png`);
      showToast(`Downloaded "${selectedSticker.name}" 128×128 Discord PNG!`);
    });

    toggleAnimatedBtn?.addEventListener("click", () => {
      isAnimatedMode = !isAnimatedMode;
      toggleAnimatedBtn.classList.toggle("anim-toggle-active", isAnimatedMode);
      if (toggleAnimatedLabel) {
        toggleAnimatedLabel.textContent = `Animated: ${isAnimatedMode ? "ON" : "OFF"}`;
      }
      renderStickerGrid();
      if (selectedSticker) updateSelectedSticker(selectedSticker, false);
      if (refreshSlangViewFn) refreshSlangViewFn();
      showToast(
        isAnimatedMode
          ? "⚡ Animated Mode ON (Looping WebP & GIF)"
          : "Static Mode ON (512px PNG & WebP)"
      );
    });

    downloadPackBtn?.addEventListener("click", exportActivePack);
    sharePackBtn?.addEventListener("click", () => directShareSticker(selectedSticker));

    shareAppBtn?.addEventListener("click", async () => {
      if (navigator.share) {
        try {
          await navigator.share({
            url: window.location.href
          });
          return;
        } catch (_) {}
      }
      showToast("PeelOff link ready to share!");
    });

    document.querySelectorAll(".nav-tab-btn").forEach((tab) => {
      tab.addEventListener("click", () => {
        const targetId = tab.getAttribute("data-nav-target");
        document.querySelectorAll(".nav-tab-btn").forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");

        if (targetId === "view-packs" || targetId === "view-slang") {
          document.querySelectorAll(".trini-subtab-btn").forEach((b) => {
            const isMatch = b.getAttribute("data-trini-subview") === targetId;
            b.classList.toggle("active", isMatch);
            b.setAttribute("aria-selected", isMatch ? "true" : "false");
          });
        }

        document.querySelectorAll(".view-panel").forEach((panel) => {
          panel.classList.toggle("active", panel.id === targetId);
        });
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    });
  }

  // Initialize App (Splash dismissal first so UI never blocks)
  initIconModal();
  renderPackRail();
  renderActivePackHeader();
  renderStickerGrid();
  if (selectedSticker) updateSelectedSticker(selectedSticker, false);
  initTriniSlangSection();
  initCaptionStudio();
  bindEvents();
})();
