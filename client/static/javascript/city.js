
    function changeCity(cityName) {
        fetch(`/booking/?city=${cityName}`)
            .then(response => response.text())
            .then(html => {
                document.body.innerHTML = html;
            });
    }

