// I have no API endpoints yet as this sort of sits outside any backend tasks we have set so far - hopefully will make Lucas do this when possible
import LoadData from "../loadData.jsx"
import { useState } from "react";



function SellerInfo({sellerID, location, setLocation}) {
    return (
        <div>
            <div className="seller name">
                <LoadData endpoint="sellerInfo/name" queryParams={{sellerID: sellerID}} />
            </div>
            <div className="seller address">
                <LoadData endpoint="sellerInfo/address" queryParams={{sellerID: sellerID, sellerLocation: location}} />
            </div>
            <div>
                <select value={location} onChange={(e) => setLocation(e.target.value)}></select>
                <option value="Exeter">Exeter</option>
                <option value="York">York</option>
                <option value="London">London</option>
            </div>
        </div>
    )
}

export default SellerInfo