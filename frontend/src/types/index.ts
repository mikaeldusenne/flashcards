export interface CardLang{
    lang: string;
    text: string;
    comment: string;
    // examples: string[];
}

export interface Card{
    langs: CardLang[];
    id: string;
}
