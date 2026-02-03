import useLoadData from '../loadDataHook.jsx';

function ReservedBundles() {

    const {bundles, loadingBundles} = useLoadData("seller/reservedBundles", {sellerID: 1});
    // returns a json object containin all bundles reserved, for each bundle:
    // name of buyer, pickup time, bundle name







}

export default ReservedBundles;