const API_BASE = "http://localhost:8000";

const form = document.getElementById("post-form");
const errorEl = document.getElementById("error");
const postsEl = document.getElementById("posts");

function renderPost(post) {
  const div = document.createElement("div");
  div.className = "post";
  div.innerHTML = `
    <div class="meta">${post.author} · ${new Date(post.created_at).toLocaleString()}</div>
    <div>${post.content}</div>
  `;
  return div;
}

async function loadPosts() {
  const res = await fetch(`${API_BASE}/posts`);
  const posts = await res.json();
  postsEl.innerHTML = "";
  posts.forEach((p) => postsEl.appendChild(renderPost(p)));
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorEl.textContent = "";

  const author = document.getElementById("author").value.trim();
  const content = document.getElementById("content").value.trim();

  try {
    const res = await fetch(`${API_BASE}/posts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ author, content }),
    });
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail ? JSON.stringify(body.detail) : `Request failed (${res.status})`);
    }
    const post = await res.json();
    postsEl.prepend(renderPost(post));
    form.reset();
  } catch (err) {
    errorEl.textContent = err.message;
  }
});

loadPosts().catch((err) => (errorEl.textContent = err.message));
