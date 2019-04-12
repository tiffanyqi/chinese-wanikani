const React = require('react');

export class Navigation extends React.Component {
    render() {
        return (
            <div className="navigation">
                <a href="/index/">Home</a>
                <a href="/learn/">Learn</a>
                <a href="/review/">Review</a>
                <a href="/characters/">Characters</a>
            </div>
        );
    }
}
