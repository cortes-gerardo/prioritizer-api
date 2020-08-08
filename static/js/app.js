// auth

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

// login & logout

const CLIENT_ID = 'VsDbNuQQopNlsE60IPR4HoYrVmzQ62Wi'
const DOMAIN = 'cortes-gerardo.us.auth0.com'

function get_domain() {
    this.protocol = window.location.protocol;
    this.host = window.location.hostname;
    this.host = this.host == 'localhost' ? this.host + ':8080' : this.host;
    return this.protocol + '//' + this.host;
}

function fill_login() {
    this.link = 'https://' + DOMAIN + '/authorize?audience=prioritizer&response_type=token&client_id=' + CLIENT_ID + '&redirect_uri=' + get_domain() + '/authorize'
    this.a = document.getElementById('login');
    this.a.href = this.link
}

function fill_logout() {
    this.link = 'https://' + DOMAIN + '/v2/logout?client_id=' + CLIENT_ID + '&returnTo=' + get_domain() + '/authorize'
    this.a = document.getElementById('logout');
    this.a.href = this.link
}