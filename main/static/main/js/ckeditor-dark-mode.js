/**
 * CKEditor Dark Mode Support
 * Automatically adjusts CKEditor theme based on user's system/browser dark mode preference
 */

(function() {
    'use strict';

    // Function to detect dark mode preference
    function isDarkMode() {
        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    // Function to apply dark mode configuration
    function applyDarkModeConfig() {
        if (typeof CKEDITOR !== 'undefined') {
            // For CKEditor 5 (used by django-ckeditor 6.x)
            // We'll use CSS variables which are already defined in dark-mode.css
            // But we can also set the UI theme if needed
            
            // Check if CKEditor instances exist
            if (CKEDITOR.instances) {
                for (var instance in CKEDITOR.instances) {
                    if (CKEDITOR.instances.hasOwnProperty(instance)) {
                        var editor = CKEDITOR.instances[instance];
                        if (editor && editor.container) {
                            // Apply dark mode class to editor container
                            if (isDarkMode()) {
                                editor.container.$.classList.add('ck-dark-mode');
                            } else {
                                editor.container.$.classList.remove('ck-dark-mode');
                            }
                        }
                    }
                }
            }

            // Configure CKEditor default config for dark mode
            if (isDarkMode()) {
                // For CKEditor 5, we use CSS variables (already handled by dark-mode.css)
                // But we can also set additional config if needed
                if (CKEDITOR.config) {
                    // Note: CKEditor 5 doesn't use 'skin' like CKEditor 4
                    // Instead, we rely on CSS custom properties
                    // The dark-mode.css file already handles this via @media queries
                }
            }
        }
    }

    // Function to handle media query changes
    function handleDarkModeChange(e) {
        applyDarkModeConfig();
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            // Wait for CKEditor to be available
            var checkCKEditor = setInterval(function() {
                if (typeof CKEDITOR !== 'undefined') {
                    clearInterval(checkCKEditor);
                    applyDarkModeConfig();
                    
                    // Listen for dark mode changes
                    if (window.matchMedia) {
                        var darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
                        // Modern browsers
                        if (darkModeQuery.addEventListener) {
                            darkModeQuery.addEventListener('change', handleDarkModeChange);
                        }
                        // Older browsers
                        else if (darkModeQuery.addListener) {
                            darkModeQuery.addListener(handleDarkModeChange);
                        }
                    }
                }
            }, 100);
            
            // Stop checking after 10 seconds
            setTimeout(function() {
                clearInterval(checkCKEditor);
            }, 10000);
        });
    } else {
        // DOM already loaded
        if (typeof CKEDITOR !== 'undefined') {
            applyDarkModeConfig();
            
            // Listen for dark mode changes
            if (window.matchMedia) {
                var darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
                if (darkModeQuery.addEventListener) {
                    darkModeQuery.addEventListener('change', handleDarkModeChange);
                } else if (darkModeQuery.addListener) {
                    darkModeQuery.addListener(handleDarkModeChange);
                }
            }
        }
    }

    // Also listen for CKEditor instance creation
    if (typeof CKEDITOR !== 'undefined') {
        CKEDITOR.on('instanceReady', function(ev) {
            applyDarkModeConfig();
        });
    }
})();

