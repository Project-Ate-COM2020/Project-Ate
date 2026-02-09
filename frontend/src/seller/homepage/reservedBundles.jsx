import useLoadData from '../loadDataHook.jsx';

function ReservedBundles() {

    const {bundles, loadingBundles} = useLoadData("seller/reservedBundles", {sellerID: 1});
    // returns a json object containin all bundles reserved, for each bundle:
    // name of buyer, pickup time, bundle name, bundle code
    
    let render_bundles;

    if (loadingBundles) {
        render_bundles = <p>Loading...</p>
    } else {
        <div>
            {bundles.map(bundle => (
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