// I have no API endpoints yet as this sort of sits outside any backend tasks we have set so far - hopefully will make Lucas do this when possible
import LoadData from "../loadData.jsx"
import "./sellerInfo.css"



function SellerInfo({sellerID, location, setLocation}) {
    return (
        <div className="seller-info-container">
            <div>
                <select className="location-dropdown-container" value={location} onChange={(e) => setLocation(e.target.value)}>
                    <option value="Exeter">Exeter</option>
                    <option value="York">York</option>
                    <option value="London">London</option>
                </select>
            </div>
            <div className="seller-name-container">
                <LoadData endpoint="seller/getsellername" queryParams={{seller_id: sellerID}} />
            </div>
            <div className="seller-address-container">
                <LoadData endpoint="seller/getselleraddress" queryParams={{seller_id: sellerID, sellerLocation: location}} />
            </div>
        </div>
    )
}

export default SellerInfo