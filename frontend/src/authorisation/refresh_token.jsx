/* --- Import Statements --- */
import usePostData from "../api/post.jsx";

/* --- File Description --- */
/* Provides a reusable way to refresh the token in the browser - 2 functions, one for sellers and one for
buyers */

/* --- Current Errors --- */
/* Need to make a way to send a get request with no implicit authorisation - as this endpoint is unprotected and trying to 
access it with an outdated token is undefined behaviour */

/* I have realised I will need to change the structure entirely to another hook - I will do this when I get the chance */

/* --- Function Definitions --- */
function refresh_token_seller() {
    // Get refresh token 
    const token = localStorage.getItem('refresh_token');

    let dataToPost = { "refresh" : token}

    const { data : refreshed_tokens, loading : loading} = usePostData("marketplace/authorismarketplace/seller/auth/token/refresh", dataToPost);
}

function refresh_token_buyer() {
    // Get refresh token 
    const token = localStorage.getItem('refresh_token');

    let dataToPost = { "refresh" : token}

    const { data : refreshed_tokens, loading : loading} = usePostData("marketplace/authorismarketplace/buyer/auth/token/refresh", dataToPost);
}

export default refresh_token_buyer;