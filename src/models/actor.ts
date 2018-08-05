export class Actor {
    public name: string;
    public synonyms: string[];
    public countryCode: string;
    public description: string;
    public references: string[];

    // Adding CFR information
    public cfrInformationAvailable: boolean;
    public cfrSuspectedState: string;
    public cfrSuspectedVictims: string[];
    public cfrTypeOfIncident: string;
    public cfrTargetSector: string;

    constructor(actorObject: any) {
        this.name = actorObject.value;
        this.synonyms = actorObject.meta.synonyms || [];
        this.description = actorObject.description;
        this.countryCode = actorObject.meta.country;
        this.references = actorObject.meta.refs;

        // Adding CFR information
        this.cfrSuspectedState = actorObject.meta['cfr-suspected-state-sponsor'];
        this.cfrSuspectedVictims = actorObject.meta['crf-suspected-victims'];
        this.cfrTypeOfIncident = actorObject.meta['cfr-type-of-incident'];
        this.cfrTargetSector = actorObject.meta['cfr-target-category'];
        this.cfrInformationAvailable =  this.cfrSuspectedState !== undefined ||
                                        this.cfrSuspectedVictims !== undefined ||
                                        this.cfrTargetSector !== undefined ||
                                        this.cfrTypeOfIncident !== undefined;
    }

    public synonymsString(): string {
        return this.synonyms.join(', ');
    }
}
