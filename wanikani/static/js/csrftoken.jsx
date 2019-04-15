import React from 'react';

import {getCookie} from './util';


export function CSRFToken() {
    const csrftoken = getCookie('csrftoken');
    return (
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
    );
};
