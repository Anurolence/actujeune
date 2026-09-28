// Actujeune - Frontend Client Application
let currentLang = localStorage.getItem("actujeune_lang") || "fr";
let clientId = localStorage.getItem("actujeune_client_id");
if (!clientId) {
  clientId = "usr_" + Math.random().toString(36).substring(2, 12) + "_" + Date.now();
  localStorage.setItem("actujeune_client_id", clientId);
}

let isDataSaver = localStorage.getItem("actujeune_data_saver") === "true";

let activeCategory = "all";
let activeRegion = "all";
let activeOppType = "all";
let activeSort = "latest";
let searchQuery = "";
let searchDebounceTimeout = null;

// DOM Elements
const postsGrid = document.getElementById("postsGrid");
const searchInput = document.getElementById("searchInput");
const categorySelect = document.getElementById("categorySelect");
const regionSelect = document.getElementById("regionSelect");
const oppTypeSelect = document.getElementById("oppTypeSelect");
const sortSelect = document.getElementById("sortSelect");
const categoryPillsContainer = document.getElementById("categoryPills");

// Modals
const postModal = document.getElementById("postModal");
const deleteModal = document.getElementById("deleteModal");
const postForm = document.getElementById("postForm");
const modalTitle = document.getElementById("modalTitle");
const modalSubmitBtn = document.getElementById("modalSubmitBtn");

let editingPostId = null;
let deletingPostId = null;

// --- Initialize ---
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initLanguageSwitcher();
  initDataSaver();
  applyLanguage(currentLang);
  fetchMetadata();
  fetchPosts();
  setupEventListeners();
});

// --- Dark / Light Theme Toggle ---
function initTheme() {
  const savedTheme = localStorage.getItem("actujeune_theme") || "light";
  applyTheme(savedTheme);

  const toggleBtn = document.getElementById("btnThemeToggle");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme") || "light";
      const next = current === "dark" ? "light" : "dark";
      applyTheme(next);
      localStorage.setItem("actujeune_theme", next);
    });
  }
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = theme === "dark" ? "☀️" : "🌙";
}

// --- Data Saver Mode (Optimized for Cameroonian Mobile Bundles) ---
function initDataSaver() {
  const toggleBtn = document.getElementById("btnDataSaver");
  if (isDataSaver) {
    document.body.classList.add("data-saver-mode");
    if (toggleBtn) toggleBtn.classList.add("active");
  }

  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      isDataSaver = !isDataSaver;
      localStorage.setItem("acujeune_data_saver", isDataSaver);
      document.body.classList.toggle("data-saver-mode", isDataSaver);
      toggleBtn.classList.toggle("active", isDataSaver);
      showToast(isDataSaver ? t('dataSaverActive') : "Mode standard activé", "info");
    });
  }
}

// --- I18n / Language handling ---
function initLanguageSwitcher() {
  const frBtn = document.getElementById("btnLangFr");
  const enBtn = document.getElementById("btnLangEn");

  if (frBtn && enBtn) {
    frBtn.addEventListener("click", () => setLanguage("fr"));
    enBtn.addEventListener("click", () => setLanguage("en"));
  }
}

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem("acujeune_lang", lang);
  applyLanguage(lang);
  fetchPosts(); // Refresh view
}

function t(key) {
  const dict = TRANSLATIONS[currentLang] || TRANSLATIONS.fr;
  return dict[key] || key;
}

function applyLanguage(lang) {
  const frBtn = document.getElementById("btnLangFr");
  const enBtn = document.getElementById("btnLangEn");

  if (frBtn && enBtn) {
    frBtn.classList.toggle("active", lang === "fr");
    enBtn.classList.toggle("active", lang === "en");
  }

  // Update text for all elements with data-i18n
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (key && TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
      el.textContent = TRANSLATIONS[lang][key];
    }
  });

  // Update placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (key && TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
      el.setAttribute("placeholder", TRANSLATIONS[lang][key]);
    }
  });
}

// --- Event Listeners ---
function setupEventListeners() {
  // Search
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      clearTimeout(searchDebounceTimeout);
      searchDebounceTimeout = setTimeout(() => {
        searchQuery = e.target.value.trim();
        fetchPosts();
      }, 300);
    });
  }

  // Select Filters
  if (categorySelect) {
    categorySelect.addEventListener("change", (e) => {
      activeCategory = e.target.value;
      updateActiveCategoryPills();
      fetchPosts();
    });
  }

  if (regionSelect) {
    regionSelect.addEventListener("change", (e) => {
      activeRegion = e.target.value;
      fetchPosts();
    });
  }

  if (oppTypeSelect) {
    oppTypeSelect.addEventListener("change", (e) => {
      activeOppType = e.target.value;
      fetchPosts();
    });
  }

  if (sortSelect) {
    sortSelect.addEventListener("change", (e) => {
      activeSort = e.target.value;
      fetchPosts();
    });
  }

  // Form submit
  if (postForm) {
    postForm.addEventListener("submit", handlePostFormSubmit);
  }

  // Image file upload handler
  const imageFileInput = document.getElementById("postImageFile");
  if (imageFileInput) {
    imageFileInput.addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      
      const formData = new FormData();
      formData.append("file", file);
      
      try {
        showToast(currentLang === "fr" ? "Téléchargement de l'image..." : "Uploading image...", "info");
        const res = await fetch("/api/upload", {
          method: "POST",
          body: formData
        });
        if (res.ok) {
          const data = await res.json();
          document.getElementById("postImageUrl").value = data.url;
          showToast(currentLang === "fr" ? "Image enregistrée !" : "Image uploaded!", "success");
        } else {
          showToast("Upload error", "error");
        }
      } catch (err) {
        console.error(err);
        showToast("Upload network error", "error");
      }
    });
  }
}

// --- Fetch Metadata (Categories, Regions, Counters) ---
async function fetchMetadata() {
  try {
    const res = await fetch("/api/meta");
    if (!res.ok) return;
    const data = await res.json();

    // Update Stats counters
    if (data.stats) {
      const elPosts = document.getElementById("statPostsCount");
      const elViews = document.getElementById("statViewsCount");
      const elLikes = document.getElementById("statLikesCount");
      const elComments = document.getElementById("statCommentsCount");

      if (elPosts) elPosts.textContent = data.stats.total_posts || 0;
      if (elViews) elViews.textContent = (data.stats.total_views || 0).toLocaleString();
      if (elLikes) elLikes.textContent = (data.stats.total_likes || 0).toLocaleString();
      if (elComments) elComments.textContent = (data.stats.total_comments || 0).toLocaleString();
    }

    // Populate category pills
    if (categoryPillsContainer && data.categories) {
      renderCategoryPills(data.categories);
    }
  } catch (err) {
    console.error("Error fetching metadata:", err);
  }
}

function renderCategoryPills(categories) {
  categoryPillsContainer.innerHTML = `
    <button class="category-pill ${activeCategory === 'all' ? 'active' : ''}" onclick="selectCategoryPill('all')">
      ${t('allCategories')}
    </button>
  `;

  categories.forEach(cat => {
    const btn = document.createElement("button");
    btn.className = `category-pill ${activeCategory === cat.category ? 'active' : ''}`;
    btn.textContent = `${cat.category} (${cat.count})`;
    btn.onclick = () => selectCategoryPill(cat.category);
    categoryPillsContainer.appendChild(btn);
  });
}

function selectCategoryPill(category) {
  activeCategory = category;
  if (categorySelect) categorySelect.value = category;
  updateActiveCategoryPills();
  fetchPosts();
}

function updateActiveCategoryPills() {
  document.querySelectorAll(".category-pill").forEach(pill => {
    if (activeCategory === "all" && pill.textContent.includes(t('allCategories'))) {
      pill.classList.add("active");
    } else if (pill.textContent.startsWith(activeCategory)) {
      pill.classList.add("active");
    } else {
      pill.classList.remove("active");
    }
  });
}

// --- Fetch Posts ---
async function fetchPosts() {
  if (!postsGrid) return;
  postsGrid.innerHTML = `
    <div style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
      <p style="color: var(--text-secondary); font-size: 1rem;">Chargement des actualités / Loading updates...</p>
    </div>
  `;

  try {
    const params = new URLSearchParams();
    if (searchQuery) params.append("search", searchQuery);
    if (activeCategory && activeCategory !== "all") params.append("category", activeCategory);
    if (activeRegion && activeRegion !== "all") params.append("region", activeRegion);
    if (activeOppType && activeOppType !== "all") params.append("opportunity_type", activeOppType);
    params.append("sort_by", activeSort);

    const res = await fetch(`/api/posts?${params.toString()}`);
    if (!res.ok) throw new Error("Failed to load posts");

    const posts = await res.json();
    renderPosts(posts);
  } catch (err) {
    console.error("Fetch posts error:", err);
    postsGrid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">⚠️</div>
        <h3>Erreur de chargement</h3>
        <p>Impossible de récupérer les actualités. Vérifiez votre connexion.</p>
      </div>
    `;
  }
}

// --- Render Posts Grid ---
function renderPosts(posts) {
  if (!postsGrid) return;

  if (!posts || posts.length === 0) {
    postsGrid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🇨🇲</div>
        <h3>${t('noPostsFound')}</h3>
        <p>${currentLang === 'fr' ? 'Soyez le premier à partager une initiative de votre région !' : 'Be the first to share an initiative from your region!'}</p>
        <button class="btn-primary" style="margin-top: 1rem;" onclick="openCreateModal()">
          ${t('postNewBtn')}
        </button>
      </div>
    `;
    return;
  }

  postsGrid.innerHTML = posts.map(post => {
    const defaultImage = "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=800&q=80";
    const imageUrl = post.image_url || defaultImage;
    const authorInitials = (post.author_name || "J").split(" ").map(n => n[0]).join("").substring(0, 2).toUpperCase();
    const tagsList = post.tags ? post.tags.split(",").map(tag => `<span class="post-tag">#${tag.trim()}</span>`).join("") : "";
    const formattedDate = new Date(post.created_at).toLocaleDateString(currentLang === "fr" ? "fr-FR" : "en-US", {
      day: "numeric",
      month: "short",
      year: "numeric"
    });

    let oppBadgeClass = "badge-opp-story";
    let oppBadgeText = t('oppTypeStory');
    if (post.opportunity_type === "concours") {
      oppBadgeClass = "badge-opp-concours";
      oppBadgeText = t('oppTypeConcours');
    } else if (post.opportunity_type === "bourse") {
      oppBadgeClass = "badge-opp-bourse";
      oppBadgeText = t('oppTypeBourse');
    } else if (post.opportunity_type === "emploi_stage") {
      oppBadgeClass = "badge-opp-emploi";
      oppBadgeText = t('oppTypeEmploi');
    }

    return `
      <article class="post-card" id="post-card-${post.id}">
        <div class="post-image-container">
          <img src="${imageUrl}" alt="${escapeHtml(post.title)}" loading="lazy" onerror="this.src='${defaultImage}'" />
          <div class="post-badges-overlay">
            ${post.is_featured ? `<span class="badge-featured">${t('featuredBadge')}</span>` : ''}
            <span class="badge-opp-type ${oppBadgeClass}">${oppBadgeText}</span>
            <span class="badge-category">${escapeHtml(post.category)}</span>
          </div>
          <span class="badge-region">📍 ${escapeHtml(post.region)}</span>
        </div>

        <div class="post-body">
          <div class="post-meta-top">
            <span>📅 ${formattedDate}</span>
            ${post.deadline ? `<span style="color: var(--cm-red); font-weight:700;">⏰ ${post.deadline}</span>` : `<span>👁️ ${post.views_count} ${t('views')}</span>`}
          </div>

          <h3 class="post-title">
            <a href="/post/${post.id}">${escapeHtml(post.title)}</a>
          </h3>

          <p class="post-summary">${escapeHtml(post.summary)}</p>

          ${post.remuneration_fcfa ? `
            <div style="margin-bottom: 0.75rem;">
              <span style="background: var(--cm-yellow-light); color: #92400e; font-weight: 700; font-size: 0.75rem; padding: 3px 8px; border-radius: var(--radius-sm);">
                💰 ${escapeHtml(post.remuneration_fcfa)}
              </span>
            </div>
          ` : ''}

          ${tagsList ? `<div class="post-tags">${tagsList}</div>` : ''}

          <div class="post-author-bar">
            <div class="author-info">
              <div class="author-avatar">${authorInitials}</div>
              <div class="author-names">
                <strong>${escapeHtml(post.author_name)}</strong>
                <small>${escapeHtml(post.author_role || 'Jeune Reporter')}</small>
              </div>
            </div>

            <div class="post-actions-bar">
              <button class="btn-card-action" onclick="toggleLike(${post.id}, this)" title="${t('like')}">
                <span class="like-icon">❤️</span>
                <span class="like-count">${post.likes_count}</span>
              </button>

              <button class="btn-card-action" onclick="shareWhatsApp(${post.id}, '${escapeHtml(post.title).replace(/'/g, "\\'")}')" title="WhatsApp 🇨🇲">
                <span style="color:#25D366; font-size:1.1rem;">💬</span>
              </button>

              <a href="/post/${post.id}#comments" class="btn-card-action" title="${t('comments')}">
                <span>💬</span>
                <span>${post.comments_count || 0}</span>
              </a>

              <button class="btn-card-action" onclick="sharePost(${post.id})" title="${t('share')}">
                <span>🔗</span>
              </button>

              <button class="btn-card-action" onclick="openEditModal(${post.id})" title="${t('edit')}">
                <span>✏️</span>
              </button>

              <button class="btn-card-action" onclick="openDeleteModal(${post.id})" title="${t('delete')}">
                <span style="color: var(--cm-red);">🗑️</span>
              </button>
            </div>
          </div>
        </div>
      </article>
    `;
  }).join("");
}

// --- CRUD: Modal Open / Close ---
function openCreateModal() {
  editingPostId = null;
  postForm.reset();
  document.getElementById("postId").value = "";
  modalTitle.textContent = t('modalCreateTitle');
  modalSubmitBtn.textContent = t('btnSubmitCreate');
  postModal.classList.add("show");
}

async function openEditModal(postId) {
  editingPostId = postId;
  modalTitle.textContent = t('modalEditTitle');
  modalSubmitBtn.textContent = t('btnSubmitUpdate');

  try {
    const res = await fetch(`/api/posts/${postId}`);
    if (!res.ok) throw new Error("Could not load post");
    const post = await res.json();

    document.getElementById("postId").value = post.id;
    document.getElementById("postTitle").value = post.title;
    document.getElementById("postOppType").value = post.opportunity_type || "story";
    document.getElementById("postSummary").value = post.summary;
    document.getElementById("postContent").value = post.content;
    document.getElementById("postCategory").value = post.category;
    document.getElementById("postRegion").value = post.region;
    document.getElementById("postDeadline").value = post.deadline || "";
    document.getElementById("postRemuneration").value = post.remuneration_fcfa || "";
    document.getElementById("postWhatsApp").value = post.contact_whatsapp || "";
    document.getElementById("postApplyLink").value = post.apply_link || "";
    document.getElementById("postAuthorName").value = post.author_name;
    document.getElementById("postAuthorRole").value = post.author_role || "";
    document.getElementById("postImageUrl").value = post.image_url || "";
    document.getElementById("postTags").value = post.tags || "";
    document.getElementById("postFeatured").checked = Boolean(post.is_featured);

    postModal.classList.add("show");
  } catch (err) {
    console.error(err);
    showToast("Error loading post data", "error");
  }
}

function closePostModal() {
  postModal.classList.remove("show");
}

function openDeleteModal(postId) {
  deletingPostId = postId;
  deleteModal.classList.add("show");
}

function closeDeleteModal() {
  deleteModal.classList.remove("show");
  deletingPostId = null;
}

// --- CRUD: Create & Update Handler ---
async function handlePostFormSubmit(e) {
  e.preventDefault();

  const payload = {
    title: document.getElementById("postTitle").value.trim(),
    summary: document.getElementById("postSummary").value.trim(),
    content: document.getElementById("postContent").value.trim(),
    category: document.getElementById("postCategory").value,
    region: document.getElementById("postRegion").value,
    opportunity_type: document.getElementById("postOppType").value,
    deadline: document.getElementById("postDeadline").value.trim() || null,
    remuneration_fcfa: document.getElementById("postRemuneration").value.trim() || null,
    contact_whatsapp: document.getElementById("postWhatsApp").value.trim() || null,
    apply_link: document.getElementById("postApplyLink").value.trim() || null,
    author_name: document.getElementById("postAuthorName").value.trim(),
    author_role: document.getElementById("postAuthorRole").value.trim() || "Jeune Leader",
    image_url: document.getElementById("postImageUrl").value.trim() || null,
    tags: document.getElementById("postTags").value.trim() || null,
    is_featured: document.getElementById("postFeatured").checked ? 1 : 0,
    status: "published"
  };

  const isEdit = Boolean(editingPostId);
  const url = isEdit ? `/api/posts/${editingPostId}` : "/api/posts";
  const method = isEdit ? "PUT" : "POST";

  try {
    modalSubmitBtn.disabled = true;
    modalSubmitBtn.textContent = isEdit ? "Enregistrement..." : "Publication...";

    const res = await fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail ? JSON.stringify(err.detail) : "Save error");
    }

    closePostModal();
    showToast(isEdit ? (currentLang === "fr" ? "Publication mise à jour !" : "Post updated!") : (currentLang === "fr" ? "Opportunité publiée avec succès !" : "Opportunity published successfully!"), "success");
    fetchMetadata();
    fetchPosts();
  } catch (err) {
    console.error("Submit error:", err);
    showToast(err.message, "error");
  } finally {
    modalSubmitBtn.disabled = false;
    modalSubmitBtn.textContent = isEdit ? t('btnSubmitUpdate') : t('btnSubmitCreate');
  }
}

// --- CRUD: Delete ---
async function confirmDeletePost() {
  if (!deletingPostId) return;

  try {
    const res = await fetch(`/api/posts/${deletingPostId}`, {
      method: "DELETE"
    });

    if (res.ok) {
      closeDeleteModal();
      showToast(currentLang === "fr" ? "Publication supprimée !" : "Post deleted!", "success");
      fetchMetadata();
      fetchPosts();
    } else {
      showToast("Error deleting post", "error");
    }
  } catch (err) {
    console.error(err);
    showToast("Network error", "error");
  }
}

// --- Interactions: Like ---
async function toggleLike(postId, btnElement) {
  try {
    const formData = new FormData();
    formData.append("client_id", clientId);

    const res = await fetch(`/api/posts/${postId}/like`, {
      method: "POST",
      body: formData
    });

    if (res.ok) {
      const data = await res.json();
      const countSpan = btnElement.querySelector(".like-count");
      if (countSpan) countSpan.textContent = data.likes_count;
      btnElement.classList.toggle("liked", data.has_liked);
      showToast(data.has_liked ? "❤️ " + t('liked') : "💔", "info");
      fetchMetadata(); // update counters
    }
  } catch (err) {
    console.error(err);
  }
}

// --- Interactions: WhatsApp Direct Share (Crucial for Cameroon) ---
function shareWhatsApp(postId, title) {
  const url = `${window.location.origin}/post/${postId}`;
  const text = encodeURIComponent(`🇨🇲 *${title}* sur Actujeune (Actualités & Opportunités Jeunesse Cameroun) :\n${url}`);
  window.open(`https://api.whatsapp.com/send?text=${text}`, '_blank');
}

// --- Interactions: Share Permalinks ---
function sharePost(postId) {
  const url = `${window.location.origin}/post/${postId}`;
  if (navigator.clipboard) {
    navigator.clipboard.writeText(url).then(() => {
      showToast(t('linkCopied'), "success");
    });
  } else {
    prompt("Copiez ce lien / Copy link:", url);
  }
}

// --- Toast notification ---
function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// --- Utility: HTML Escape ---
function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
}
