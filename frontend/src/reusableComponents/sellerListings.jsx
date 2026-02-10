// bascically very similar to Listings.jsx but differentiated so as nt to interfere with Will's code

import { useEffect, useState } from "react";

export default function SellerListings({seller}) {
  const [bundles, setBundles] = useState([]);

  const fakeBundles = [
    { id: 1, name: "Student Bundle", price: 9.99 },
    { id: 2, name: "Meal Prep Bundle", price: 14.5 },
    { id: 3, name: "Family Bundle", price: 24.99 },
  ];


  useEffect(() => {
    let bundles  = fetch(`/bundles?${seller}`) 
    setBundles(bundles) // reformatted Will's code - think this is slightly more readable
  }, [seller]); // currently use expliceit live_bundles

  const bundleElements = []; // this is an array of the divs, each one is a bundle
  for (let i = 0; i < fakeBundles.length; i++) {
    const bundle = fakeBundles[i];
    bundleElements.push(
      <div key={bundle.id}>
        <h3>{bundle.name}</h3>
        <p>£{bundle.price}</p>
        <p>Stock remaining: {bundle.stock}</p>
        <p>Sales: {bundle.sales}</p>
        <p>Reservations in progress: {bundle.reservations}</p>
      </div>
    );
  }

  return (
    // this is just a div containing all the bundle elements
    <div>
      {bundleElements}
    </div>
  );
}