function resizePlotlyGraphs() {
  if (window.Plotly) {
    document.querySelectorAll(".plotly-graph-div").forEach(function(div) {
      div.style.width = "100%";
      div.style.height = "100%";

      setTimeout(function() {
        Plotly.Plots.resize(div);
      }, 10);
    });
  }
}

function debounce(func, wait) {
  let timeout;
  return function() {
    const context = this;
    const args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function() {
      func.apply(context, args);
    }, wait);
  };
}

document.addEventListener("DOMContentLoaded", function() {
  resizePlotlyGraphs();

  const popup = document.getElementById("popupContainer");
  const overlay = document.getElementById("popupOverlay");
  const popupBtn = document.getElementById("popupButton");

  if (popup && overlay) {
    popup.style.display = "block";
    overlay.style.display = "block";
  }

  function closePopup() {
    if (popup && overlay) {
      popup.style.display = "none";
      overlay.style.display = "none";
    }
  }

  if (popupBtn) {
    popupBtn.addEventListener("click", closePopup);
  }
  if (closeBtn) {
    closeBtn.addEventListener("click", closePopup);
  }
});

window.addEventListener("resize", debounce(function() {
  resizePlotlyGraphs();
}, 250));
