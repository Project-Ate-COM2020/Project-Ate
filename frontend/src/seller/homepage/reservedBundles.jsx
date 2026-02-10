import useLoadData from '../loadDataHook.jsx';
import { useState } from "react";

function ReservedBundles() {
    try{
        const {data, loading} = useLoadData("seller/reservedBundles", {sellerID: 1});
    }
    // returns a json object containin all bundles reserved, for each bundle:
    // name of buyer, pickup time, bundle name, bundle code
    
    let render_bundles = false;

    if (loading) {
        render_bundles = <p>Loading...</p>
    } else {
        render_bundles =
        <div>
            {data.map(bundle => (
                <div key={bundle.id}>
                    <p>Buyer: {bundle.buyer}</p>
                    <p>Pickup time: {bundle.time}</p>
                    <p>Bundle: {bundle.name}</p>
                    <p>Code: {bundle.code}</p>
                </div>
            ))}
        </div>
    }


    return (
        render_bundles
    )




}

export default ReservedBundles;