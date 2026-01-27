/* The nav bar goes at the top of the page to help navigate the website
add in the links to the different webpages needed and badges*/

/* -profile - home - login - basket - orders */

export default function NavBar() {
    return (
      <nav>
        <a href ="/">Project-Ate</a>
        <ul>
            <li><a href="/">profile</a></li>    
            <li><a href="/">bakset</a> </li>   
            <li><a href="/">login</a></li>    
            <li><a href="/">orders</a></li>     
            
        </ul>
      </nav>
    );
  }
  
