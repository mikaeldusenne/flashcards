export interface CardLang {
  lang: string;
  text: string;
  comment: string;
  // examples: string[];
}

export interface Card {
  langs: CardLang[];
  decks: string[];
    id: string;
    creator: string;
    difficulty: number;
    importance: number;
    created: Date;
    modified: Date;
}
