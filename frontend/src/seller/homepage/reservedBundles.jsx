import useLoadData from '../loadDataHook.jsx';
import { useState } from "react";
import './reservedBundles.css';

function ReservedBundles() {
    const {data, loading} = useLoadData("seller/getreservations", {seller_id: 1});
    // returns a json object containin all bundles reserved, for each bundle:
    // name of buyer, pickup time, bundle name, bundle code
    
    let render_bundles = false;

    if (loading) {
        render_bundles = <p>Loading...</p>
    } else {
        console.log("data: ");
        console.log(data);
        render_bundles =
        <div className = "reservedBundles-panel">
            {data.upcoming_reservations.map(bundle => (
                <div key={bundle.reservation_id}>
                    <p>Buyer: {bundle.consumer_name}</p>
                    <p>Pickup time: {bundle.reservation_time}</p>
                    <p>Bundle: {bundle.Posting_id}</p>
                    <p>Code: {bundle.reservation_code}</p>
                    <hr />
                </div>
            ))}
        </div>
    }


    return (
        render_bundles
    )




}

export default ReservedBundles;