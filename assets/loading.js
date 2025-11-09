window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    hide_overlay: function(value) {
      const overlay = document.getElementById('loading-overlay');
      if (overlay) {
        setTimeout(() => overlay.classList.remove('active'), 800);
      }
      return window.dash_clientside.no_update;
    }
  }
});
