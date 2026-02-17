function switchPhoto(url, thumb) {
    document.getElementById('mainImg').src = url;
    document.querySelectorAll('.gallery-thumb').forEach(t => t.classList.remove('active'));
    thumb.classList.add('active');
}

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("toggle-specs");
    const extraSpecs = document.querySelectorAll(".extra-spec");

    if (btn) {
      btn.addEventListener("click", function () {
        const isHidden = extraSpecs[0]?.classList.contains("hidden-spec");

        extraSpecs.forEach(spec => {
          spec.classList.toggle("hidden-spec");
        });

        btn.textContent = isHidden ? "Mostra meno" : "Mostra tutte";
      });
    }
  });