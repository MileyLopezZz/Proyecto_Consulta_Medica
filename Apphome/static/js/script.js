// Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
  // ==========================================
  // MENÚ MÓVIL
  // ==========================================
  const mobileMenuBtn = document.getElementById("mobileMenuBtn")
  const navMenu = document.querySelector(".nav-menu")

  if (mobileMenuBtn && navMenu) {
    mobileMenuBtn.addEventListener("click", function () {
      this.classList.toggle("active")
      navMenu.classList.toggle("active")
    })

    // Cerrar menú al hacer clic en un enlace
    const navLinks = navMenu.querySelectorAll("a")
    navLinks.forEach((link) => {
      link.addEventListener("click", () => {
        mobileMenuBtn.classList.remove("active")
        navMenu.classList.remove("active")
      })
    })
  }

  // ==========================================
  // CARRUSEL DE SERVICIOS - INFINITE SCROLL
  // ==========================================
    const carouselTrack = document.getElementById("carouselTrack")
    const prevBtn = document.getElementById("prevBtn")
    const nextBtn = document.getElementById("nextBtn")
    const indicatorsContainer = document.getElementById("carouselIndicators")

  if (carouselTrack && prevBtn && nextBtn) {
    const originalCards = Array.from(carouselTrack.querySelectorAll(".service-card"))
    let currentIndex = 1 // Start at 1 for infinite scroll
    let isTransitioning = false

    function setupInfiniteScroll() {
      // Clear existing cards
      carouselTrack.innerHTML = ""

      // Clone last card and add to beginning
      const lastClone = originalCards[originalCards.length - 1].cloneNode(true)
      carouselTrack.appendChild(lastClone)

      // Add all original cards
      originalCards.forEach((card) => {
        carouselTrack.appendChild(card.cloneNode(true))
      })

      // Clone first card and add to end
      const firstClone = originalCards[0].cloneNode(true)
      carouselTrack.appendChild(firstClone)

      // Set initial position without transition
      updateCarouselPosition(false)
    }

    function updateCarouselPosition(withTransition = true) {
      if (withTransition) {
        carouselTrack.style.transition = "transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)"
      } else {
        carouselTrack.style.transition = "none"
      }

      const offset = -currentIndex * 100
      carouselTrack.style.transform = `translateX(${offset}%)`

      updateIndicators()
    }

    function createIndicators() {
      if (!indicatorsContainer) return

      indicatorsContainer.innerHTML = ""

      originalCards.forEach((_, index) => {
        const indicator = document.createElement("button")
        indicator.classList.add("carousel-indicator")
        indicator.setAttribute("aria-label", `Go to slide ${index + 1}`)
        indicator.addEventListener("click", () => goToSlide(index))
        indicatorsContainer.appendChild(indicator)
      })

      updateIndicators()
    }

    function updateIndicators() {
      const indicators = indicatorsContainer?.querySelectorAll(".carousel-indicator")
      if (!indicators) return

      let activeIndex = currentIndex - 1

      // Handle infinite scroll wrap-around
      if (currentIndex === 0) {
        activeIndex = originalCards.length - 1
      } else if (currentIndex === originalCards.length + 1) {
        activeIndex = 0
      }

      indicators.forEach((indicator, index) => {
        indicator.classList.toggle("active", index === activeIndex)
      })
    }

    function goToSlide(index) {
      if (isTransitioning) return
      isTransitioning = true
      currentIndex = index + 1 // +1 because of the cloned card at the beginning
      updateCarouselPosition(true)
      setTimeout(() => {
        isTransitioning = false
      }, 500)
    }

    function handleTransitionEnd() {
      if (currentIndex === 0) {
        currentIndex = originalCards.length
        updateCarouselPosition(false)
      } else if (currentIndex === originalCards.length + 1) {
        currentIndex = 1
        updateCarouselPosition(false)
      }
      isTransitioning = false
    }

    carouselTrack.addEventListener("transitionend", handleTransitionEnd)

    prevBtn.addEventListener("click", () => {
      if (isTransitioning) return
      isTransitioning = true
      currentIndex--
      updateCarouselPosition(true)
    })

    nextBtn.addEventListener("click", () => {
      if (isTransitioning) return
      isTransitioning = true
      currentIndex++
      updateCarouselPosition(true)
    })

    let touchStartX = 0
    let touchEndX = 0

    carouselTrack.addEventListener(
      "touchstart",
      (e) => {
        touchStartX = e.changedTouches[0].screenX
      },
      { passive: true },
    )

    carouselTrack.addEventListener(
      "touchend",
      (e) => {
        touchEndX = e.changedTouches[0].screenX
        handleSwipe()
      },
      { passive: true },
    )

    function handleSwipe() {
      const swipeThreshold = 50
      const diff = touchStartX - touchEndX

      if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
          nextBtn.click()
        } else {
          prevBtn.click()
        }
      }
    }

    let autoplayInterval

    function startAutoplay() {
      autoplayInterval = setInterval(() => {
        if (!isTransitioning) {
          nextBtn.click()
        }
      }, 5000)
    }

    function stopAutoplay() {
      clearInterval(autoplayInterval)
    }

    // Pause autoplay on hover/interaction
    carouselTrack.addEventListener("mouseenter", stopAutoplay)
    carouselTrack.addEventListener("mouseleave", startAutoplay)

    prevBtn.addEventListener("click", () => {
      stopAutoplay()
      setTimeout(startAutoplay, 10000)
    })

    nextBtn.addEventListener("click", () => {
      stopAutoplay()
      setTimeout(startAutoplay, 10000)
    })

    // Initialize carousel
    setupInfiniteScroll()
    createIndicators()
    startAutoplay()
  }

  // ==========================================
  // FORMULARIO DE CONTACTO
  // ==========================================
  const contactForm = document.getElementById("contactForm")

  if (contactForm) {
    contactForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Obtener valores del formulario
      const name = document.getElementById("contactName").value
      const email = document.getElementById("contactEmail").value
      const phone = document.getElementById("contactPhone").value
      const message = document.getElementById("contactMessage").value

      // Aquí puedes agregar la lógica para enviar el formulario
      // Por ejemplo, usando fetch para enviar a tu backend Django

      console.log("Formulario enviado:", { name, email, phone, message })

      // Mostrar mensaje de éxito (puedes personalizar esto)
      alert("¡Gracias por contactarnos! Te responderemos pronto.")

      // Limpiar formulario
      contactForm.reset()
    })
  }

  // ==========================================
  // SCROLL SUAVE PARA ENLACES DE NAVEGACIÓN
  // ==========================================
  const smoothScrollLinks = document.querySelectorAll('a[href^="#"]')

  smoothScrollLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const href = this.getAttribute("href")

      // Ignorar enlaces que solo son "#"
      if (href === "#") return

      e.preventDefault()

      const targetId = href.substring(1)
      const targetElement = document.getElementById(targetId)

      if (targetElement) {
        const headerOffset = 80 // Altura del header sticky
        const elementPosition = targetElement.getBoundingClientRect().top
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset

        window.scrollTo({
          top: offsetPosition,
          behavior: "smooth",
        })
      }
    })
  })

  // ==========================================
  // HEADER STICKY CON SOMBRA AL HACER SCROLL
  // ==========================================
  const header = document.querySelector(".main-header")

  if (header) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 50) {
        header.style.boxShadow = "0 2px 8px rgba(0, 0, 0, 0.1)"
      } else {
        header.style.boxShadow = "none"
      }
    })
  }

  // ==========================================
  // ANIMACIÓN DE ENTRADA PARA ELEMENTOS
  // ==========================================
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1"
        entry.target.style.transform = "translateY(0)"
      }
    })
  }, observerOptions)

  // Aplicar animación a las tarjetas de servicio
    const serviceCards = document.querySelectorAll(".service-card")
        serviceCards.forEach((card) => {
            card.style.opacity = "0"
            card.style.transform = "translateY(20px)"
            card.style.transition = "opacity 0.6s ease, transform 0.6s ease"
            observer.observe(card)
    })

  // Aplicar animación a los items de contacto
    const contactItems = document.querySelectorAll(".contact-item")
        contactItems.forEach((item) => {
            item.style.opacity = "0"
            item.style.transform = "translateY(20px)"
            item.style.transition = "opacity 0.6s ease, transform 0.6s ease"
            observer.observe(item)
    })
})


document.addEventListener("DOMContentLoaded", () => {
  const dropdown = document.getElementById("portalDropdown");
  const toggle = dropdown.querySelector(".dropdown-toggle");
  const menu = dropdown.querySelector(".dropdown-menu");

  // Abrir/cerrar el menú al hacer clic en el botón
  toggle.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropdown.classList.toggle("open");
  });

  // Cerrar si haces clic fuera
  document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove("open");
    }
  });
});

// ==== Eliminar alertas automáticamente después de 3 segundos ====
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => alert.remove());
  }, 3000);
});


