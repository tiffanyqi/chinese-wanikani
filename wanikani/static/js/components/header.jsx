import React from 'react';
import {Link} from 'react-router-dom';

export function Header() {
    return (
        <header>
            <nav>
                <ul>
                    <li><Link to="/index">Home</Link></li>
                    <li><Link to="/learn">Learn</Link></li>
                    <li><Link to="/review">Review</Link></li>
                    <li><Link to="/characters">Characters</Link></li>
                </ul>
            </nav>
        </header>
    );
}
