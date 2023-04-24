function getQuote() {
    const motivationalQuotes = [
    {
        "author":"Martin Luther King Jr.",
        "quote":"Out of the mountain of despair, a stone of hope."
    },
    {
        "author":"When you have a dream, you've got to grab it and never let it go.",
        "quote":"Carol Burnett"
    },
    {
        "author":"Audrey Hepburn",
        "quote":"Nothing is impossible. The world itself says I'm possible!"
    },
    {
        "author":"Alexander the Great",
        "quote":"There is nothing impossible to they who will try."
    },
    {
        "author":"Micheal Altshuler",
        "quote":"The bad news is that time flies. The good news is you're the pilot."
    },
    {
        "author":"Nicole Kidman",
        "quote":"Life has got  all those twists and turns. You've got to hold on tight and off you go."
    },
    {
        "author":"Walt Whitman",
        "quote":"Keep your face always toward the sunshine, and shadows will fall behind you."
    },
    {
        "author":"Amal Clooney",
        "quote":"Be courageous. Challenge orthodoxy. Stand up for what you believe in."
    },
    {
        "author":"Winston Churchill",
        "quote":"Success is not final, failure is not fatal: it is courage to continue that counts."
    },
    {
        "author":"Oprah Winfrey",
        "quote":"You define your own life. Don't let other people write your script."
    },
    {
        "author":"Malala Yousafzai",
        "quote":"You are never too old to set another goal or to dream a new dream."
    },
    {
        "author":"Michelle Obama",
        "quote":"For me, becoming isn’t about arriving somewhere or achieving a certain aim. I see it instead as forward motion, a means of evolving, a way to reach continuously toward a better self. The journey doesn't end."
    },
    {
        "author":"Mother Teresa",
        "quote":"Spread love everywhere you go."
    },
    {
        "author":"Lady Gaga",
        "quote":"Do not allow people to dim your shine because they are blinded. Tell them to put some sunglasses on."
    },
    {
        "author":"Gabrielle Bernstein",
        "quote":"If you make your internal life a priority, then everything else you need on the outside will be given to you and it will be extremely clear what the next step is."
    },
    {
        "author":"Mandy Hale",
        "quote":"You don't always need a plan. Sometimes you just need to breathe, trust, let go and see what happens."
    },
    {
        "author":"Kesha",
        "quote":"You can be everything. You can be the infinite amount of things that people are."
    },
    {
        "author":"Ralph Waldo Emerson",
        "quote":"What lies behind you and what lies in front of you, pales in comparison to what lies inside of you."
    },
    {
        "author":"Alexandria Ocasio-Cortez",
        "quote":"I am experienced enough to do this. I am knowledgeable enough to do this. I am prepared enough to do this. I am mature enough to do this. I am brave enough to do this."
    },
    {
        "author":"Robin Williams",
        "quote":"No matter what people tell you, words and ideas can change the world."
    },
    {
        "author":"Aristotle",
        "quote":"It is during our darkest moments that we must focus to see the light."
    },
    {
        "author":"Marie Forleo",
        "quote":"Not having the best situation, but seeing the best in your situation is the key to happiness."
    },
    {
        "author":"Theodore Roosevelt",
        "quote":"Believe you can and you're halfway there."
    },
    {
        "author":"Marianne Cantwell",
        "quote":"Weaknesses are just strengths in the wrong environment."
    },
    {
        "author":"Ella Fitzgerald",
        "quote":"Just don't give up trying to do what you really want to do. Where there is love and inspiration, I don't think you can go wrong."
    },
    {
        "author":"Maya Angelou",
        "quote":"Try to be a rainbow in someone's cloud."
    },
    {
        "author":"Mahatma Gandhi",
        "quote":"In a gentle way, you can shake the world."
    },
    {
        "author":"Morgan Freeman",
        "quote":"Learning how to be still, to really be still and let life happen—that stillness becomes a radiance."
    },
    {
        "author":"Earl Nightingale",
        "quote":"All you need is the plan, the road map, and the courage to press on to your destination."
    },
    {
        "author":"Pink",
        "quote":"I care about decency and humanity and kindness. Kindness today is an act of rebellion."
    },
    {
        "author":"Joseph Campbell",
        "quote":"We must let go of the life we have planned, so as to accept the one that is waiting for us."
    },
    {
        "author":"Ruth Bader Ginsburg",
        "quote":"Real change, enduring change, happens one step at a time."
    },
    {
        "author":"Dwayne 'The Rock' Johnson",
        "quote":"Wake up determined, go to bed satisfied."
    },
    {
        "author":"Albert Einstein",
        "quote":"Life is like riding a bicycle. To keep your balance, you must keep moving."
    },
    {
        "author":"Dolly Parton",
        "quote":"If you don't like the road you're walking, start paving another one!"
    },
    {
        "author":"Amy Dickinson",
        "quote":"We are not our best intentions. We are what we do."
    },
    {
        "author":"Tina Turner",
        "quote":"I believe that if you'll just stand up and go, life will open up for you. Something just motivates you to keep moving."
    },
    {
        "author":"Franklin Delano Roosevelt",
        "quote":"The only limit to our realization of tomorrow will be our doubts today."
    },
    {
        "author":"Camilla Eyring Kimball",
        "quote":"You do not find the happy life. You make it."
    }
]


const randomNum = Math.floor(Math.random() * motivationalQuotes.length);

const randomQuote = motivationalQuotes[randomNum];

var quote = randomQuote;

document.getElementById('quote').innerHTML = randomQuote.quote + " Spoken by: " + randomQuote.author;

}

window.onload = getQuote
