// ==========================================
// TYPING ANIMATION
// ==========================================

const typingText = document.getElementById("typing-text");

const roles = [
    "AI & Machine Learning",
    "Computer Vision",
    "Data Science",
    "Python Developer"
];

let roleIndex = 0;
let characterIndex = 0;
let deleting = false;

function typeRole() {
    const currentRole = roles[roleIndex];

    if (!deleting) {
        typingText.textContent = currentRole.substring(
            0,
            characterIndex + 1
        );

        characterIndex++;

        if (characterIndex === currentRole.length) {
            deleting = true;

            setTimeout(typeRole, 1800);
            return;
        }

        setTimeout(typeRole, 90);

    } else {
        typingText.textContent = currentRole.substring(
            0,
            characterIndex - 1
        );

        characterIndex--;

        if (characterIndex === 0) {
            deleting = false;

            roleIndex++;

            if (roleIndex === roles.length) {
                roleIndex = 0;
            }

            setTimeout(typeRole, 400);
            return;
        }

        setTimeout(typeRole, 45);
    }
}

if (typingText) {
    typeRole();
}


// ==========================================
// MOBILE NAVIGATION
// ==========================================

const menuToggle = document.getElementById("menuToggle");
const navMenu = document.querySelector(".nav-menu");

if (menuToggle && navMenu) {

    menuToggle.addEventListener("click", () => {
        navMenu.classList.toggle("show");
        menuToggle.classList.toggle("open");
    });

}


// ==========================================
// CLOSE MOBILE MENU AFTER CLICK
// ==========================================

const navLinks = document.querySelectorAll(".nav-link");

navLinks.forEach((link) => {

    link.addEventListener("click", () => {

        if (navMenu) {
            navMenu.classList.remove("show");
        }

        if (menuToggle) {
            menuToggle.classList.remove("open");
        }

    });

});


// ==========================================
// ACTIVE NAVIGATION LINK
// ==========================================

const sections = document.querySelectorAll("section[id]");

function updateActiveLink() {

    const scrollPosition = window.scrollY + 150;

    sections.forEach((section) => {

        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute("id");

        if (
            scrollPosition >= sectionTop &&
            scrollPosition < sectionTop + sectionHeight
        ) {

            navLinks.forEach((link) => {
                link.classList.remove("active");
            });

            const activeLink = document.querySelector(
                `.nav-link[href="#${sectionId}"]`
            );

            if (activeLink) {
                activeLink.classList.add("active");
            }
        }

    });
}

window.addEventListener("scroll", updateActiveLink);


// ==========================================
// SCROLL REVEAL ANIMATION
// ==========================================

const revealElements = document.querySelectorAll(
    ".section-heading, .about-text, .stat-box, .skill-card, .project-card, .contact-info, .contact-action"
);

const revealObserver = new IntersectionObserver(
    (entries, observer) => {

        entries.forEach((entry) => {

            if (entry.isIntersecting) {

                entry.target.classList.add("revealed");

                observer.unobserve(entry.target);
            }

        });

    },
    {
        threshold: 0.12
    }
);

revealElements.forEach((element) => {
    element.classList.add("reveal");
    revealObserver.observe(element);
});


// ==========================================
// PROJECT CARD TILT EFFECT
// ==========================================

const projectCards = document.querySelectorAll(".project-card");

projectCards.forEach((card) => {

    card.addEventListener("mousemove", (event) => {

        if (window.innerWidth <= 760) {
            return;
        }

        const rect = card.getBoundingClientRect();

        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -2;
        const rotateY = ((x - centerX) / centerX) * 2;

        card.style.transform =
            `perspective(800px)
             rotateX(${rotateX}deg)
             rotateY(${rotateY}deg)
             translateY(-8px)`;
    });


    card.addEventListener("mouseleave", () => {

        card.style.transform = "";

    });

});


// ==========================================
// NAVBAR SCROLL EFFECT
// ==========================================

const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () => {

    if (!navbar) {
        return;
    }

    if (window.scrollY > 40) {

        navbar.classList.add("scrolled");

    } else {

        navbar.classList.remove("scrolled");

    }

});


// ==========================================
// CURRENT YEAR
// ==========================================

const yearElement = document.querySelector(".copyright");

if (yearElement) {

    const currentYear = new Date().getFullYear();

    yearElement.innerHTML =
        `© ${currentYear} Sohaib Khan. All rights reserved.`;

}
// ==========================================
// CERTIFICATE IMAGE MODAL
// ==========================================

const certificateModal =
    document.getElementById("certificateModal");

const modalImage =
    document.getElementById("modalImage");

const modalClose =
    document.getElementById("modalClose");

const certificateButtons =
    document.querySelectorAll(".certificate-view");


certificateButtons.forEach((button) => {

    button.addEventListener("click", () => {

        const imagePath =
            button.getAttribute("data-image");

        if (!certificateModal || !modalImage) {
            return;
        }

        modalImage.src = imagePath;

        certificateModal.classList.add("show");

        document.body.style.overflow = "hidden";
    });

});


if (modalClose) {

    modalClose.addEventListener("click", closeCertificateModal);

}


if (certificateModal) {

    certificateModal.addEventListener("click", (event) => {

        if (event.target === certificateModal) {
            closeCertificateModal();
        }

    });

}


function closeCertificateModal() {

    if (!certificateModal) {
        return;
    }

    certificateModal.classList.remove("show");

    document.body.style.overflow = "";

}

// ==========================================
// PROJECT FILTERS AND VIDEO MODAL
// ==========================================

const projectFilters = document.querySelectorAll(".project-filter");
const fullProjectCards = document.querySelectorAll(".project-full-card");
const projectVideoModal = document.getElementById("projectVideoModal");
const projectVideo = document.getElementById("projectVideo");
const projectVideoClose = document.getElementById("projectVideoClose");

function openProjectVideo(card) {
    if (!projectVideoModal || !projectVideo) {
        return;
    }

    projectVideo.src = card.dataset.video;
    projectVideoModal.classList.add("show");
    projectVideoModal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    projectVideo.play().catch(() => {});
}

function closeProjectVideo() {
    if (!projectVideoModal || !projectVideo) {
        return;
    }

    projectVideo.pause();
    projectVideo.removeAttribute("src");
    projectVideo.load();
    projectVideoModal.classList.remove("show");
    projectVideoModal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
}

projectFilters.forEach((filter) => {
    filter.addEventListener("click", () => {
        const selectedCategory = filter.dataset.filter;

        projectFilters.forEach((button) => {
            button.classList.toggle("active", button === filter);
        });

        fullProjectCards.forEach((card) => {
            const shouldShow = selectedCategory === "all" ||
                card.dataset.category === selectedCategory;
            card.classList.toggle("is-hidden", !shouldShow);
        });
    });
});

fullProjectCards.forEach((card) => {
    card.addEventListener("click", (event) => {
        if (event.target.closest("a")) {
            return;
        }

        openProjectVideo(card);
    });

    card.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            openProjectVideo(card);
        }
    });
});

if (projectVideoModal) {
    projectVideoModal.addEventListener("click", (event) => {
        if (event.target === projectVideoModal) {
            closeProjectVideo();
        }
    });

    projectVideoModal.addEventListener("contextmenu", (event) => {
        event.preventDefault();
    });
}

if (projectVideoClose) {
    projectVideoClose.addEventListener("click", closeProjectVideo);
}

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && projectVideoModal?.classList.contains("show")) {
        closeProjectVideo();
    }
});


// ==========================================
// AUTO-HIDE CONTACT FORM MESSAGES
// ==========================================

document.querySelectorAll(".flash-message").forEach((message) => {
    setTimeout(() => {
        message.classList.add("is-hiding");

        setTimeout(() => {
            message.remove();
        }, 350);
    }, 3000);
});
