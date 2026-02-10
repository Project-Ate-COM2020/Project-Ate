/* The nav bar goes at the top of the page to help navigate the website
add in the links to the different webpages needed and badges*/

import './navBar.css';

// future hooks to get streak length and bagdes displayed and well a custom user name 

export default function NavBar() {
    return (
      <nav>
        <a href ="/user">Project-Ate</a>
        <ul>
            <li><a href="/">Profile</a></li>    
            {/*<li><a href="/basket">Bakset</a> </li>*/}
            <li><a href="/">Login</a></li>    
            <li><a href="/orders">Orders</a></li>     
            
        </ul>
      </nav>
    );
  }
  
