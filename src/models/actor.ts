export class Actor {
    public name: string;
    public synonyms: string[];
    public countryCode: string;
    public description: string;
    public references: string[];

    constructor(actorObject: any) {
        this.name = actorObject.value;
        this.synonyms = actorObject.meta.synonyms;
        this.description = actorObject.description;
        this.countryCode = actorObject.meta.country;
        this.references = actorObject.meta.refs;
    }

    public synonymsString(): string {
        return this.synonyms.join(', ');
    }
}
