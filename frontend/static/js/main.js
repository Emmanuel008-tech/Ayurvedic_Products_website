/**
 * AyuDhara - Main Interactive Scripts (Vanilla JS)
 * Handles:
 * - Background video cycling (Hero banner) without manual pill indicators
 * - Sticky header blur on scroll
 * - Mobile navigation menu toggle
 * - Dynamic WhatsApp message generation on public contact form
 * - Custom Admin Dashboard: live image preview & mobile sidebar toggle
 */

document.addEventListener('DOMContentLoaded', () => {

  /* --------------------------------------------------------------------------
     1. Seamless Background Video Cycling (Hero Banner)
     -------------------------------------------------------------------------- */
  const heroVideos = [
    document.getElementById('heroVideo0'),
    document.getElementById('heroVideo1'),
    document.getElementById('heroVideo2')
  ].filter(Boolean);

  let currentVideoIndex = 0;
  let videoTimer = null;

  function switchVideo(nextIndex) {
    if (heroVideos.length <= 1) return;

    const currentVid = heroVideos[currentVideoIndex];
    const nextVid = heroVideos[nextIndex];

    if (!currentVid || !nextVid) return;

    // Start playing the next video
    nextVid.currentTime = 0;
    const playPromise = nextVid.play();
    if (playPromise !== undefined) {
      playPromise.then(() => {
        nextVid.classList.add('active');
        currentVid.classList.remove('active');
        currentVideoIndex = nextIndex;
      }).catch(() => {
        // Fallback if browser throttles autoplay
        nextVid.classList.add('active');
        currentVid.classList.remove('active');
        currentVideoIndex = nextIndex;
      });
    }
  }

  function startVideoAutoplayCycle() {
    if (heroVideos.length <= 1) return;
    if (videoTimer) clearInterval(videoTimer);

    videoTimer = setInterval(() => {
      const nextIndex = (currentVideoIndex + 1) % heroVideos.length;
      switchVideo(nextIndex);
    }, 7000); // Transitions smoothly every 7 seconds
  }

  if (heroVideos.length > 0) {
    startVideoAutoplayCycle();
  }

  /* --------------------------------------------------------------------------
     2. Sticky Header Scroll Effect
     -------------------------------------------------------------------------- */
  const siteHeader = document.getElementById('siteHeader');
  if (siteHeader) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 40) {
        siteHeader.classList.add('scrolled');
      } else {
        siteHeader.classList.remove('scrolled');
      }
    }, { passive: true });
  }

  /* --------------------------------------------------------------------------
     3. Public Mobile Navigation Toggle
     -------------------------------------------------------------------------- */
  const mobileNavToggle = document.getElementById('mobileNavToggle');
  const navLinks = document.getElementById('navLinks');

  if (mobileNavToggle && navLinks) {
    mobileNavToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('open');
      mobileNavToggle.setAttribute('aria-expanded', isOpen);
    });

    // Close mobile menu on link click
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        mobileNavToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* --------------------------------------------------------------------------
     4. Dynamic WhatsApp URL Generation on Contact Form
     -------------------------------------------------------------------------- */
  const nameInput = document.getElementById('id_name');
  const phoneInput = document.getElementById('id_phone_number');
  const productSelect = document.getElementById('id_product');
  const messageInput = document.getElementById('id_message');
  const dynamicWaLink = document.getElementById('dynamicWaSubmitLink');

  const bizNumber = '919778256391';

  function updateDynamicWaLink() {
    if (!dynamicWaLink) return;

    const name = nameInput ? nameInput.value.trim() : '';
    const phone = phoneInput ? phoneInput.value.trim() : '';
    const message = messageInput ? messageInput.value.trim() : '';
    let productName = 'General Enquiry';

    if (productSelect && productSelect.selectedIndex > 0) {
      productName = productSelect.options[productSelect.selectedIndex].text;
    }

    let text = `Namaste AyuDhara! 🙏\n\nI am interested in enquiring about:\n📦 *${productName}*\n`;
    if (name) text += `\n👤 Name: ${name}`;
    if (phone) text += `\n📞 Phone: ${phone}`;
    if (message) text += `\n💬 Note: ${message}`;
    text += `\n\nPlease let me know about availability and delivery details. Thank you!`;

    dynamicWaLink.href = `https://wa.me/${bizNumber}?text=${encodeURIComponent(text)}`;
  }

  if (nameInput) nameInput.addEventListener('input', updateDynamicWaLink);
  if (phoneInput) phoneInput.addEventListener('input', updateDynamicWaLink);
  if (productSelect) productSelect.addEventListener('change', updateDynamicWaLink);
  if (messageInput) messageInput.addEventListener('input', updateDynamicWaLink);

  // Initialize once on page load
  updateDynamicWaLink();

  /* --------------------------------------------------------------------------
     5. Custom Admin Dashboard: Live Image Preview
     -------------------------------------------------------------------------- */
  const imageInput = document.getElementById('id_image');
  const liveImagePreview = document.getElementById('liveImagePreview');

  if (imageInput && liveImagePreview) {
    imageInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (event) => {
          liveImagePreview.src = event.target.result;
          liveImagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  /* --------------------------------------------------------------------------
     6. Custom Admin Dashboard: Mobile Sidebar Toggle
     -------------------------------------------------------------------------- */
  const dashboardMobileToggle = document.getElementById('dashboardMobileToggle');
  const dashboardSidebar = document.getElementById('dashboardSidebar');

  if (dashboardMobileToggle && dashboardSidebar) {
    dashboardMobileToggle.addEventListener('click', () => {
      dashboardSidebar.classList.toggle('open');
    });

    // Close when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 768 && 
          !dashboardSidebar.contains(e.target) && 
          !dashboardMobileToggle.contains(e.target)) {
        dashboardSidebar.classList.remove('open');
      }
    });
  }

});
