const API_URL = "http://159.89.215.206:8012";
let form = document.getElementById('form');
let value1 = document.getElementById('search');


function getRatingColor(rating) {
    if (rating >= 7) {
        return 'green';
    } else if (rating >= 4) {
        return 'grey';
    } else {
        return 'red';
    }
}

function film_view(films){

    const filmList = document.getElementById("films");

    for (const film of films) {
        const filmDiv = document.createElement("div");
        filmDiv.className = "film";

        const filmPoster = document.createElement("div");
        filmPoster.className = "film-poster";

        const images = film.image.map(image => {
            const img = document.createElement("img");
            img.src = image.image_url;
            img.width = 100;
            return img;
        }
        );
        for (const image of images) {
            filmPoster.appendChild(image);
        }

        filmDiv.appendChild(filmPoster);

        const filmInfo = document.createElement("div");
        filmInfo.className = "film-info";
        filmInfo.innerHTML = `
            <h3>${film.title} (${film.year})</h3>
            <p>Director: ${film.director}</p>
        `;

        const categories = film.categories.map(category => category.category_name.toLowerCase()).join(', ');
        const categoriesText = document.createTextNode(`Categories: ${categories}`);
        filmInfo.appendChild(categoriesText);
        filmInfo.appendChild(document.createElement("br"));

        const actors = film.cast.map(actor => `${actor.first_name} ${actor.last_name}`).join(', ');
        const actorsText = document.createTextNode(`Actors: ${actors}`);
        filmInfo.appendChild(actorsText);

        filmDiv.appendChild(filmInfo);

        const filmRating = document.createElement("div");
        filmRating.className = "film-rating";
        filmRating.textContent = `IMDb: ${film.rating}`;
        filmRating.style.color = getRatingColor(film.rating);
        filmDiv.appendChild(filmRating);

        filmList.appendChild(filmDiv);
    }
}
function clearBox()
{
    document.getElementById('films').innerHTML = "";
}
async function fetchFilms() {
    const response = await fetch(`${API_URL}/films`);
    if (!response.ok) {
        console.error("Error fetching films:", response.status, response.statusText);
        return;
    }
    const films = await response.json();
    clearBox();
    film_view(films);

}

async function event(value){
   response = await fetch(`${API_URL}/films/search?name=${value}`);
   if (!response.ok) {
       console.error("Error fetching films:", response.status, response.statusText);
       return;
   }
   const films = await response.json();
   clearBox();
   film_view(films);
}
form.addEventListener("submit", (e) => {
    e.preventDefault();

    let value = value1.value;
    event(value);
})
fetchFilms();
