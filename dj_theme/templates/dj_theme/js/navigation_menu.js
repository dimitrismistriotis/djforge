(function () {
    /* Toggle Sidebar */
    const sidebar = document.getElementById("sidebar");

    if (sidebar) {
        function toggleSidebarMobile(
            sidebar,
            sidebarBackdrop,
            toggleSidebarMobileHamburger,
            toggleSidebarMobileClose
        ) {
            sidebar.classList.toggle("hidden");
            sidebarBackdrop.classList.toggle("hidden");
            toggleSidebarMobileHamburger.classList.toggle("hidden");
            toggleSidebarMobileClose.classList.toggle("hidden");
        }

        const toggleSidebarMobileEl = document.getElementById(
            "toggleSidebarMobile"
        );
        const sidebarBackdrop = document.getElementById("sidebarBackdrop");
        const toggleSidebarMobileHamburger = document.getElementById(
            "toggleSidebarMobileHamburger"
        );
        const toggleSidebarMobileClose = document.getElementById(
            "toggleSidebarMobileClose"
        );
        {% comment %}
        // Search not present in current implementation,
        // when aside is collapsed, it displays one on top
        const toggleSidebarMobileSearch = document.getElementById(
            "toggleSidebarMobileSearch"
        );

        toggleSidebarMobileSearch.addEventListener("click", function () {
            toggleSidebarMobile(
                sidebar,
                sidebarBackdrop,
                toggleSidebarMobileHamburger,
                toggleSidebarMobileClose
            );
        }); {% endcomment %}

        toggleSidebarMobileEl.addEventListener("click", function () {
            toggleSidebarMobile(
                sidebar,
                sidebarBackdrop,
                toggleSidebarMobileHamburger,
                toggleSidebarMobileClose
            );
        });

        sidebarBackdrop.addEventListener("click", function () {
            toggleSidebarMobile(
                sidebar,
                sidebarBackdrop,
                toggleSidebarMobileHamburger,
                toggleSidebarMobileClose
            );
        });
    }
})();
