const apiBaseUrls = {
    auth: "http://localhost:8000/api/users",
    posts: "http://localhost:8001/api/posts",
    likes: "http://localhost:8002/api/likes",
    comments: "http://localhost:8003/api/comments"
};

// Helper function to redirect
function redirectTo(url) {
    window.location.href = url;
}

// Login Function
function loginUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch(`${apiBaseUrls.auth}/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem("token", data.token);  // Save token to localStorage
            redirectTo("dashboard.html");  // Redirect to dashboard
        } else {
            document.getElementById("login-message").textContent = "Invalid credentials. Try again.";
        }
    })
    .catch(error => console.error("Error:", error));
}

// Logout Function
function logoutUser() {
    localStorage.removeItem("token");
    redirectTo("login.html");
}

// Fetch and Display Posts
function fetchPosts() {
    const token = localStorage.getItem("token");
    fetch(`${apiBaseUrls.posts}/`, {
        method: "GET",
        headers: { "Authorization": `Token ${token}` }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Fetched posts data:", data);  // Debugging: Log the fetched posts
        displayPosts(data);  // Pass data to displayPosts function
    })
    .catch(error => console.error("Error fetching posts:", error));
}

// Display Posts with Likes and Comments
function displayPosts(posts) {
    const container = document.getElementById("posts-container");
    container.innerHTML = "";  // Clear existing posts

    posts.forEach(post => {
        console.log("Rendering post with ID:", post.id);  // Debugging: Log each post ID

        const postElement = document.createElement("div");
        postElement.className = "post";
        postElement.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.content}</p>
            <p>Author: ${post.author}</p>
            <p>Likes: <span id="likes-count-${post.id}">${post.likes_count}</span></p>
            <button onclick="likePost(${post.id})">Like</button>  <!-- Pass post.id here -->
            <button onclick="fetchComments(${post.id})">Show Comments</button> <!-- Pass post.id here -->
            <div id="comments-${post.id}" class="comments-section"></div>
            <input type="text" id="comment-input-${post.id}" placeholder="Add a comment">
            <button onclick="addComment(${post.id})">Comment</button>
        `;
        container.appendChild(postElement);
    });
}

// Create a New Post
function createPost() {
    const token = localStorage.getItem("token");
    const title = prompt("Enter post title:");
    const content = prompt("Enter post content:");

    fetch(`${apiBaseUrls.posts}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Token ${token}`
        },
        body: JSON.stringify({ title, content })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Post created:", data);  // Debugging: Log the created post
        fetchPosts();  // Refresh posts after creating a new one
    })
    .catch(error => console.error("Error creating post:", error));
}

// Like a Post
function likePost(postId) {
    console.log("Like postId:", postId);  // Debugging: Log postId
    if (!postId) {
        console.error("Post ID is undefined in likePost function");
    }
    const token = localStorage.getItem("token");
    fetch(`${apiBaseUrls.likes}/like/${postId}/`, {
        method: "POST",
        headers: { "Authorization": `Token ${token}` }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Liked post:", data);
        fetchPosts();  // Re-fetch all posts to update the like count
    })
    .catch(error => console.error("Error liking post:", error));
}

// Fetch Comments for a Post
function fetchComments(postId) {
    console.log("Fetch comments for postId:", postId);  // Debugging: Log postId
    if (!postId) {
        console.error("Post ID is undefined in fetchComments function");
    }
    fetch(`${apiBaseUrls.comments}/list/${postId}/`, {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
        console.log("Fetched comments:", data);  // Debugging: Log comments data
        displayComments(postId, data);
    })
    .catch(error => console.error("Error fetching comments:", error));
}

// Display Comments
function displayComments(postId, comments) {
    const commentsSection = document.getElementById(`comments-${postId}`);
    commentsSection.innerHTML = "";  // Clear existing comments

    comments.forEach(comment => {
        const commentElement = document.createElement("p");
        commentElement.textContent = `${comment.user}: ${comment.content}`;
        commentsSection.appendChild(commentElement);
    });
}

// Add a Comment to a Post
function addComment(postId) {
    const token = localStorage.getItem("token");
    const content = document.getElementById(`comment-input-${postId}`).value;

    fetch(`${apiBaseUrls.comments}/add/${postId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Token ${token}`
        },
        body: JSON.stringify({ content })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Comment added:", data);  // Debugging: Log added comment
        fetchComments(postId);  // Refresh comments after adding a new one
    })
    .catch(error => console.error("Error adding comment:", error));
}

// Load Posts on Dashboard
if (window.location.pathname.endsWith("dashboard.html")) {
    fetchPosts();
}
