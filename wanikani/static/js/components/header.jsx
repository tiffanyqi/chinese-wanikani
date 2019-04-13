import React from 'react';
import {Link} from 'react-router-dom';

export function Header() {
    return (
        <header>
            <nav>
                <ul>
                    <li><Link to='/home'>Home</Link></li>
                    <li><Link to='/roster'>Roster</Link></li>
                    <li><Link to='/schedule'>Schedule</Link></li>
                </ul>
            </nav>
            {/* <li><Link to="/index/">Home</Link></li>
            <li><Link to="/learn/">Learn</Link></li>
            <li><Link to="/review/">Review</Link></li>
            <li><Link to="/characters/">Characters</Link></li> */}
        </header>
    );
}
