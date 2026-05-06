import sys

file_path = 'c:/Users/sumit/Desktop/ANTIGRAVITY/INCOGNITECH/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# CSS changes
css_target = '''        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
    </style>'''
css_replace = '''        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
        
        .light-theme {
            background-color: #f3f4f6 !important;
            color: #111827 !important;
        }
        .light-theme .bg-incogni-black, .light-theme nav { background-color: #ffffff !important; color: #111827 !important; border-color: rgba(0,0,0,0.1) !important;}
        .light-theme .text-white, .light-theme .text-incogni-white { color: #111827 !important; }
        .light-theme .text-gray-300 { color: #4b5563 !important; }
        .light-theme .text-gray-400 { color: #6b7280 !important; }
        .light-theme .bg-white\\/10 { background-color: rgba(0,0,0,0.05) !important; border-color: rgba(0,0,0,0.1) !important; color: #111827 !important; }
        .light-theme .bg-white\\/5 { background-color: #ffffff !important; border-color: rgba(0,0,0,0.1) !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        .light-theme input, .light-theme textarea, .light-theme select { color: #111827 !important; background-color: #ffffff !important; }
        .light-theme .floating-shapes .shape { opacity: 0.1; }
        .light-theme .morphing-bg .from-incogni-red\\/10 { opacity: 0; }
    </style>'''
content = content.replace(css_target, css_replace)

# Navbar changes
nav_target = '''                        <button onclick="handleLogout()"
                            class="text-xs text-red-400 hover:text-red-300 ml-2">Logout</button>
                    </div>
                    <button id="join-now-btn"'''
nav_replace = '''                        <button onclick="showPage('profile')" class="text-xs text-blue-400 hover:text-blue-300 ml-4">Profile</button>
                        <button onclick="handleLogout()"
                            class="text-xs text-red-400 hover:text-red-300 ml-2">Logout</button>
                    </div>
                    <button id="theme-toggle" class="p-2 rounded-full hover:bg-white/10 transition-colors ml-2 mr-2" onclick="toggleTheme()">
                        <svg id="theme-toggle-icon" class="w-5 h-5 text-incogni-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
                    </button>
                    <button id="join-now-btn"'''
content = content.replace(nav_target, nav_replace)

# Profile HTML changes
profile_target = '''            <div class="mt-6 text-center text-sm text-gray-400">
                <span id="auth-switch-text">Don't have an account?</span>
                <button onclick="toggleAuthMode()" class="text-incogni-white hover:underline ml-1 font-semibold"
                    id="auth-switch-btn">Sign up</button>
            </div>
        </div>
    </div>

    <!-- HOME PAGE -->'''
profile_replace = '''            <div class="mt-6 text-center text-sm text-gray-400">
                <span id="auth-switch-text">Don't have an account?</span>
                <button onclick="toggleAuthMode()" class="text-incogni-white hover:underline ml-1 font-semibold"
                    id="auth-switch-btn">Sign up</button>
            </div>
        </div>
    </div>

    <!-- PROFILE PAGE -->
    <section id="profile" class="page min-h-screen pt-24 pb-12 px-4 hidden">
        <div class="max-w-3xl mx-auto">
            <h2 class="text-3xl font-bold text-incogni-white mb-8">My Profile</h2>
            <div class="bg-white/5 backdrop-blur-sm border border-incogni-white/20 rounded-3xl p-8">
                <form id="profile-form" onsubmit="handleProfileUpdate(event)" class="space-y-6">
                    <div class="flex items-center space-x-6 mb-8">
                        <div class="w-24 h-24 bg-white/10 rounded-full flex items-center justify-center overflow-hidden border-2 border-incogni-white">
                            <img id="profile-avatar-preview" src="" class="hidden w-full h-full object-cover">
                            <span id="profile-initial-preview" class="text-4xl font-bold text-white">U</span>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-300 mb-2">Profile Picture</label>
                            <input type="file" id="profile-avatar-upload" accept="image/*" class="text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-white/10 file:text-incogni-white hover:file:bg-white/20">
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-300 mb-2">Full Name</label>
                        <input type="text" id="profile-name" class="w-full px-4 py-3 bg-white/10 border border-incogni-white/30 rounded-lg text-white focus:border-incogni-white focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-300 mb-2">Email Address (Read-only)</label>
                        <input type="email" id="profile-email" readonly class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-gray-400 cursor-not-allowed">
                    </div>
                    <button type="submit" id="profile-submit-btn" class="bg-incogni-white text-incogni-black px-8 py-3 rounded-full font-bold hover:bg-incogni-silver transition-colors">
                        Save Changes
                    </button>
                </form>
            </div>
        </div>
    </section>

    <!-- HOME PAGE -->'''
content = content.replace(profile_target, profile_replace)

# JavaScript changes
js_target = '''            try {
                if (context === 'pitch') {
                    // Collect Pitch Data
                    const name = currentUser ? currentUser.name : form.querySelector('input[placeholder="e.g., TechNova"]').value;
                    const email = currentUser ? currentUser.email : "pitch@example.com";
                    const message = `Pitch Name: ${form.querySelector('input[placeholder="e.g., TechNova"]').value}\\n` +
                        `Industry: ${form.querySelector('select').value}\\n` +
                        `Funding: ${form.querySelector('input[placeholder="e.g., ₹50,000"]').value}\\n` +
                        `Description: ${form.querySelector('textarea').value}`;

                    await fetchWithAuth('/contact', {
                        method: 'POST',
                        body: JSON.stringify({ name, email, message })
                    });
                } else if (context === 'notes' || context === 'project') {
                    if (!currentUser || currentUser.role !== 'admin') {
                        throw new Error('Only admins can publish notes/projects at this time.');
                    }

                    const formData = new FormData();
                    formData.append('title', form.querySelector('input[placeholder="e.g., Complete OS Notes"]').value);
                    formData.append('description', form.querySelector('textarea').value);

                    // For the single image input (if exists)
                    const fileInput = form.querySelector('input[type="file"]');
                    if (fileInput && fileInput.files[0]) {
                        formData.append('image', fileInput.files[0]);
                    }

                    // Note: 'content' is required in Blog schema
                    formData.append('content', `Uploaded via: ${context}\\nPrice Tracker: ${form.querySelector('input[placeholder="e.g., ₹99"]').value}`);

                    await fetchWithAuth('/blogs', {
                        method: 'POST',
                        body: formData // Uses FormData, so fetchWithAuth won't set Content-Type header
                    });
                }'''
js_replace = '''            try {
                if (context === 'pitch') {
                    // Collect Pitch Data
                    const inputs = form.querySelectorAll('input');
                    const selects = form.querySelectorAll('select');
                    const textareas = form.querySelectorAll('textarea');
                    
                    const startupName = inputs[0] ? inputs[0].value : 'Unknown Startup';
                    const industry = selects[0] ? selects[0].value : 'Unknown Industry';
                    const funding = inputs[1] ? inputs[1].value : 'Not specified';
                    const description = textareas[0] ? textareas[0].value : 'No description';

                    const name = currentUser ? currentUser.name : startupName;
                    const email = currentUser ? currentUser.email : "pitch@example.com";
                    
                    const message = `Pitch Name: ${startupName}\\nIndustry: ${industry}\\nFunding: ${funding}\\nDescription: ${description}`;

                    await fetchWithAuth('/contact', {
                        method: 'POST',
                        body: JSON.stringify({ name, email, message })
                    });
                } else if (context === 'notes' || context === 'project') {
                    if (!currentUser) {
                        throw new Error('Please login to publish notes or projects.');
                    }

                    const inputs = form.querySelectorAll('input:not([type="file"])');
                    const textareas = form.querySelectorAll('textarea');
                    
                    const title = inputs[0] ? inputs[0].value : 'Untitled';
                    const price = inputs[1] ? inputs[1].value : 'Free';
                    const description = textareas[0] ? textareas[0].value : 'No description';

                    const formData = new FormData();
                    formData.append('title', title);
                    formData.append('description', description);

                    // For the single image input (if exists)
                    const fileInput = form.querySelector('input[type="file"]');
                    if (fileInput && fileInput.files[0]) {
                        formData.append('image', fileInput.files[0]);
                    }

                    // Note: 'content' is required in Blog schema
                    formData.append('content', `Uploaded via: ${context}\\nPrice Tracker: ${price}`);

                    await fetchWithAuth('/blogs', {
                        method: 'POST',
                        body: formData // Uses FormData, so fetchWithAuth won't set Content-Type header
                    });
                }'''
content = content.replace(js_target, js_replace)

js_append = '''

        // Profile logic
        async function handleProfileUpdate(event) {
            event.preventDefault();
            const submitBtn = document.getElementById('profile-submit-btn');
            const originalText = submitBtn.textContent;
            submitBtn.innerHTML = '<span class="loading-spinner"></span> Saving...';
            submitBtn.disabled = true;

            try {
                const formData = new FormData();
                formData.append('name', document.getElementById('profile-name').value);
                
                const fileInput = document.getElementById('profile-avatar-upload');
                if (fileInput.files[0]) {
                    formData.append('avatar', fileInput.files[0]);
                }

                const data = await fetchWithAuth('/profile', {
                    method: 'POST',
                    body: formData
                });
                
                // Update local storage and UI
                currentUser.name = data.name;
                if (data.avatar) currentUser.avatar = data.avatar;
                localStorage.setItem('incogni_user', JSON.stringify(currentUser));
                updateUIForAuth(true);
                alert('Profile updated successfully!');
            } catch (err) {
                alert('Error updating profile: ' + err.message);
            } finally {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }
        }

        // Initialize Profile page
        function initProfilePage() {
            if (currentUser) {
                document.getElementById('profile-name').value = currentUser.name;
                document.getElementById('profile-email').value = currentUser.email;
                if (currentUser.avatar) {
                    document.getElementById('profile-initial-preview').classList.add('hidden');
                    document.getElementById('profile-avatar-preview').src = currentUser.avatar;
                    document.getElementById('profile-avatar-preview').classList.remove('hidden');
                } else {
                    document.getElementById('profile-initial-preview').textContent = currentUser.name.charAt(0).toUpperCase();
                }
            }
        }
        
        // Theme toggle logic
        let isLightMode = false;
        function toggleTheme() {
            isLightMode = !isLightMode;
            document.body.classList.toggle('light-theme', isLightMode);
            const icon = document.getElementById('theme-toggle-icon');
            if (isLightMode) {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>';
            } else {
                icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>';
            }
        }

        // Override showPage to init profile if needed
        const originalShowPage = showPage;
        showPage = function(pageId) {
            originalShowPage(pageId);
            if (pageId === 'profile') {
                if (!currentUser) {
                    alert("Please login first to view your profile.");
                    showAuthModal();
                    originalShowPage('home');
                    return;
                }
                initProfilePage();
            }
        }
    </script>
'''
content = content.replace('    </script>', js_append)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done modifying index.html')
