/* --- File Description --- */
/* Also Following Will's Description to some extent, this file act more as a preview for the seller - allow some small actions to be made - and allow 
the seller to breakout into dedicated pages such as analytics and bundleCreation. 

Includes: 
 - Seller info
 - Analytics
 - Seller Bundle Postings
 - Seller Bundle Reservations
 - Seller Bundle Post Creation + Forecasting
 
 each of these will be split up into helper functions for readability and maintainability
 */

 /* --- Current Issues --- */

 /* The main issue is the current backend bug preventing from loggin in - this means when the backend is fixed 
and endpoints refactored, the endpoints and maybe the parsing for this file will also need to change */

/* --- Helper Functions --- */

function SellerInfo() {
    return (
        <div className = "sellerInfo">
            <p>Seller Info</p>
        </div>
    )
}

function Analytics() {
    return (
        <div className = "analytics">
            <p>Analytics</p>
        </div>
    )
}

function BundlePostings() {
    return (
        <div className = "bundlePostings">
            <p>Bundle Postings</p>
        </div>
    )
}

function BundleReservations() {
    return (
        <div className = "bundleReservations">
            <p>Bundle Reservations</p>
        </div>
    )
}

function BundlePostCreation() {
    return (
        <div className = "BundlePostCreation">
            <p>Bundle Post Creation</p>
        </div>
    )
}

/* --- Main Page Function --- */

function SellerHomePage() {
    return (
        <div>
            <SellerInfo />
            <Analytics />
            <BundlePostings />
            <BundleReservations />
            <BundlePostCreation />
        </div>
    )

}

export default BundleReservations;