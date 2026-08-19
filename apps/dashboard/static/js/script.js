function resizePlotlyGraphs() {
  if (!window.Plotly) {
    return;
  }

  document.querySelectorAll(".plotly-graph-div").forEach((graph) => {
    graph.style.width = "100%";
    graph.style.height = "100%";

    window.setTimeout(() => {
      window.Plotly.Plots.resize(graph);
    }, 10);
  });
}

function debounce(func, wait) {
  let timeoutId;

  return (...args) => {
    window.clearTimeout(timeoutId);
    timeoutId = window.setTimeout(() => {
      func(...args);
    }, wait);
  };
}

document.addEventListener("DOMContentLoaded", () => {
  resizePlotlyGraphs();

  const agentSelect = document.getElementById("agentSelect");
  const agentSelectForm = document.getElementById("agentSelectForm");
  const popup = document.getElementById("popupContainer");
  const overlay = document.getElementById("popupOverlay");
  const popupBtn = document.getElementById("popupButton");

  if (agentSelect && agentSelectForm) {
    agentSelect.addEventListener("change", () => {
      agentSelectForm.submit();
    });
  }

  if (popup && overlay) {
    popup.hidden = false;
    overlay.hidden = false;
  }

  const closePopup = () => {
    if (popup && overlay) {
      popup.hidden = true;
      overlay.hidden = true;
    }
  };

  if (popupBtn) {
    popupBtn.addEventListener("click", closePopup);
  }
});

window.addEventListener("resize", debounce(() => {
  resizePlotlyGraphs();
}, 250));
