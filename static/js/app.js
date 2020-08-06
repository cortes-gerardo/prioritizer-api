const JWTS_LOCAL_KEY = 'JWTS_LOCAL_KEY';

// invoked in app.component on load
function check_token_fragment() {
    // parse the fragment
    const fragment = window.location.hash.substr(1).split('&')[0].split('=');
    // check if the fragment includes the access token
    if (fragment[0] === 'access_token') {
        // add the access token to the jwt
        this.token = fragment[1];
        // save jwts to localstore
        this.set_jwt();
    }
}

function set_jwt() {
    localStorage.setItem(JWTS_LOCAL_KEY, this.token);
}

function load_jwts() {
    this.token = localStorage.getItem(JWTS_LOCAL_KEY) || null;

    document.getElementById('jwt').value = this.token;
}

function logout() {
    this.token = '';
    this.set_jwt();
}