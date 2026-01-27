/*lists all the avable bundle postings to the user*/

import { useEffect, useState } from "react";

export default function Listings() {
  const [bundles, setBundles] = useState([]);

  const fakeBundles = [
    { id: 1, name: "Student Bundle", price: 9.99 },
    { id: 2, name: "Meal Prep Bundle", price: 14.5 },
    { id: 3, name: "Family Bundle", price: 24.99 },
  ];


  useEffect(() => {
    fetch("/api/bundles") // need to connect to json to get all bundle postings
      .then(res => res.json())
      .then(data => setBundles(data));
  }, []);

  return (
    <div>
      <h2>Available Bundles</h2>

      {fakeBundles.map(bundle => (
        <div key={bundle.id}>
          <h3>{bundle.name}</h3>
          <p>£{bundle.price}</p>
          <button onClick={() => alert("Add link to info page")}>
            Info
          </button>

          <button onClick={() => alert("Add link to info page") }>
            Add to Cart
          </button>
        </div>
      ))}
    </div>
  );
}