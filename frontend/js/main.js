/**
 * Vanam Ayurveda - Main Interactive Scripts (Vanilla JS)
 */

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Navigation Menu Toggle
  const mobileToggle = document.getElementById('mobileNavToggle');
  const navLinks = document.getElementById('navLinks');

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.contains('is-open');
      if (isOpen) {
        navLinks.classList.remove('is-open');
        mobileToggle.setAttribute('aria-expanded', 'false');
      } else {
        navLinks.classList.add('is-open');
        mobileToggle.setAttribute('aria-expanded', 'true');
      }
    });

    // Close menu when clicking outside or clicking a nav link
    document.addEventListener('click', (e) => {
      if (!navLinks.contains(e.target) && !mobileToggle.contains(e.target)) {
        navLinks.classList.remove('is-open');
        mobileToggle.setAttribute('aria-expanded', 'false');
      }
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('is-open');
        mobileToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Pre-select product in Enquiry Form when clicking "Quick Enquiry" button on a product card
  const enquiryBtns = document.querySelectorAll('.js-enquire-btn');
  const productSelect = document.getElementById('id_product');
  const contactSection = document.getElementById('contact');

  enquiryBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const productId = btn.getAttribute('data-product-id');
      if (productSelect && productId) {
        productSelect.value = productId;
        
        // Highlight form control temporarily
        productSelect.classList.add('highlight-select');
        setTimeout(() => {
          productSelect.classList.remove('highlight-select');
        }, 1500);
      }

      if (contactSection) {
        contactSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Dynamic WhatsApp helper update when typing into enquiry form
  const nameInput = document.getElementById('id_name');
  const phoneInput = document.getElementById('id_phone_number');
  const messageInput = document.getElementById('id_message');
  const dynamicWaLink = document.getElementById('dynamicWaSubmitLink');

  function updateDynamicWhatsAppUrl() {
    if (!dynamicWaLink) return;
    
    const selectedOpt = productSelect ? productSelect.options[productSelect.selectedIndex] : null;
    const productName = (selectedOpt && selectedOpt.value) ? selectedOpt.text : 'Ayurvedic Product';
    const custName = nameInput ? nameInput.value.trim() : '';
    const custPhone = phoneInput ? phoneInput.value.trim() : '';
    const custMsg = messageInput ? messageInput.value.trim() : '';

    const bizNumber = '919778256391';
    let text = `Namaste Vanam Ayurveda! 🙏\n\nI am interested in enquiring about:\n📦 *${productName}*\n`;
    if (custName) text += `\n👤 Name: ${custName}`;
    if (custPhone) text += `\n📞 Phone: ${custPhone}`;
    if (custMsg) text += `\n💬 Note: ${custMsg}`;
    text += `\n\nPlease send details. Thank you!`;

    const encodedText = encodeURIComponent(text);
    dynamicWaLink.href = `https://wa.me/${bizNumber}?text=${encodedText}`;
  }

  if (dynamicWaLink) {
    [nameInput, phoneInput, messageInput, productSelect].forEach(element => {
      if (element) {
        element.addEventListener('input', updateDynamicWhatsAppUrl);
        element.addEventListener('change', updateDynamicWhatsAppUrl);
      }
    });
  }

  // Cinematic Sequential Background Video Carousel for Hero Banner
  const videoElements = [
    document.getElementById('heroVideo0'),
    document.getElementById('heroVideo1'),
    document.getElementById('heroVideo2')
  ].filter(Boolean);

  const indicatorBtns = document.querySelectorAll('#heroVideoControls .video-pill-btn');

  if (videoElements.length > 0) {
    let currentIdx = 0;
    let fallbackTimeout = null;

    function activateVideo(index) {
      if (fallbackTimeout) {
        clearTimeout(fallbackTimeout);
        fallbackTimeout = null;
      }

      currentIdx = (index + videoElements.length) % videoElements.length;

      videoElements.forEach((vid, i) => {
        if (i === currentIdx) {
          vid.currentTime = 0;
          vid.classList.add('active');
          const playPromise = vid.play();
          if (playPromise !== undefined) {
            playPromise.catch(err => {
              console.log('Autoplay handled:', err);
            });
          }

          // Fallback timer based on duration
          if (vid.duration && !isNaN(vid.duration)) {
            fallbackTimeout = setTimeout(() => {
              if (i === currentIdx) {
                activateVideo(i + 1);
              }
            }, (vid.duration + 0.5) * 1000);
          }
        } else {
          vid.classList.remove('active');
          setTimeout(() => {
            if (!vid.classList.contains('active')) {
              vid.pause();
            }
          }, 1400);
        }
      });

      // Update indicator button states
      indicatorBtns.forEach((btn, i) => {
        if (i === currentIdx) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });
    }

    // Attach ended event listener to each video
    videoElements.forEach((vid, idx) => {
      vid.addEventListener('ended', () => {
        activateVideo(idx + 1);
      });
    });

    // Allow user to click any video pill to switch videos
    indicatorBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const targetIdx = parseInt(btn.getAttribute('data-video-index'), 10);
        if (!isNaN(targetIdx)) {
          activateVideo(targetIdx);
        }
      });
    });

    // Start playback
    activateVideo(0);
  }

});
