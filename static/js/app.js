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

function get_domain() {
    this.protocol = window.location.protocol;
    this.host = window.location.hostname;
    this.host = this.host == 'localhost' ? this.host + ':8080' : this.host;
    return this.protocol + '//' + this.host;
}

function fill_login_href() {
    this.domain = 'https://cortes-gerardo.us.auth0.com/authorize?audience=prioritizer&response_type=token&client_id=VsDbNuQQopNlsE60IPR4HoYrVmzQ62Wi&redirect_uri=' + get_domain() + '/authorize'
    this.a = document.getElementById('login'); //or grab it by tagname etc
    this.a.href = this.domain
}