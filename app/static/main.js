function warning() {
    alert('please enter [0~8] and unrepeated values , and contain zero !');
}
var moves = data['astar'];
var curr = data['curr'];
function initial(curr, container) {
    for (let i = 0; i < 9; i++) {
        switch (curr[i]) {
            case 0: container.innerHTML += `<div class='sq sq0'></div>`; break;
            case 1: container.innerHTML += `<div class='sq sq1'>1</div>`; break;
            case 2: container.innerHTML += `<div class='sq sq2'>2</div>`; break;
            case 3: container.innerHTML += `<div class='sq sq3'>3</div>`; break;
            case 4: container.innerHTML += `<div class='sq sq4'>4</div>`; break;
            case 5: container.innerHTML += `<div class='sq sq5'>5</div>`; break;
            case 6: container.innerHTML += `<div class='sq sq6'>6</div>`; break;
            case 7: container.innerHTML += `<div class='sq sq7'>7</div>`; break;
            case 8: container.innerHTML += `<div class='sq sq8'>8</div>`; break;
        }
    }

};
function check() {
    var list = document.querySelectorAll('.sq').values;
    let count=0;
    list.forEach(element, () => {
        if (element == 0) {
            count++;
        }
    });
    if(count==2){
        return true;
    }else return false;
}
function get_index_zero(postions) {
    let index = 0;
    for (let i = 0; i < 9; i++) {
        if (postions[i] == "sq0") {
            return index;
        }
        index++;
    }
}
function move(moves) {
    list_postions = document.querySelectorAll('.sq');
    var postions = {};
    let i = 0;
    list_postions.forEach(element => {
        postions[i] = element.classList[1];
        i++;
    });
    index_zero = get_index_zero(postions);
    iter = setInterval(() => {

        if (moves[i] == "R") {
            postions = swap(index_zero, index_zero += 1, postions, i);
        } else if (moves[i] == "L") {
            postions = swap(index_zero, index_zero -= 1, postions, i);
        } else if (moves[i] == "U") {
            postions = swap(index_zero, index_zero -= 3, postions, i);
        } else if (moves[i] == "D") {
            postions = swap(index_zero, index_zero += 3, postions, i);
        }
        if (i == moves.length) {
            clearInterval(iter);
        }
        i++;
    }, 1000, i = 0);


}

function swap(index_zero, index_item, postions, i) {

    let class_goal = "." + postions[index_item];
    let zero = document.querySelector('.container .sq0');
    let item = document.querySelector(".container " + class_goal);
    let goal_value = document.querySelector(class_goal).textContent;
    item.innerHTML = "";
    zero.innerHTML = goal_value;
    item.classList.toggle(postions[index_item]);
    item.classList.add("sq0")
    zero.classList.toggle("sq0");
    zero.classList.add(postions[index_item]);
    postions[index_zero] = postions[index_item];
    postions[index_item] = "sq0";
    render(postions, i);
    return postions;
}
function get_data() {
    nodes = document.querySelectorAll('.sq');
    data = [];
    for (let i = 0; i < 9; i++) {
        data[i] = nodes.item(i).textContent;
    }
    return data;
}
function render(state, j) {
    data = get_data();
    document.querySelector('.viewer').innerHTML += `<div class="puzzel puzzel${j}">`;
    for (let i = 0; i < 9; i++) {
        document.querySelector('.puzzel' + j).innerHTML += `<div class="${state[i]}">${data[i]}</div>`;
    }
    document.querySelector('.viewer').innerHTML += `</div>`;
}
function view() {
    document.querySelector('.form-container').style.display = "none";
    document.querySelector('.pro-container').classList.add('show-pro-container');
    document.getElementById('new').addEventListener('click', () => {
        window.location.replace("http://127.0.0.1:8000/");
    })
}
