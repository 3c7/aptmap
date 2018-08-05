export class Actor {
    public name: string;
    public synonyms: string[];
    public operatingFrom: string;
    public description: string;
    public references: string[];

    // Adding CFR information
    public cfrInformationAvailable: boolean;
    public cfrSuspectedState: string;
    public cfrSuspectedVictims: string[];
    public cfrTypeOfIncident: string;
    public cfrTargetSector: string;

    // Adding iso country codes to seperate variables
    public ccOperatingFrom: string;
    public ccVictims: string[];

    constructor(actorObject: any) {
        this.name = actorObject.value;
        this.synonyms = actorObject.meta.synonyms || [];
        this.description = actorObject.description;
        this.operatingFrom = actorObject.meta.country;
        this.references = actorObject.meta.refs;

        // Adding CFR information
        this.cfrSuspectedState = actorObject.meta['cfr-suspected-state-sponsor'];
        this.cfrSuspectedVictims = actorObject.meta['cfr-suspected-victims'];
        this.cfrTypeOfIncident = actorObject.meta['cfr-type-of-incident'];
        this.cfrTargetSector = actorObject.meta['cfr-target-category'];
        this.cfrInformationAvailable =  this.cfrSuspectedState !== undefined ||
                                        this.cfrSuspectedVictims !== undefined ||
                                        this.cfrTargetSector !== undefined ||
                                        this.cfrTypeOfIncident !== undefined;

        // Adding iso country codes to seperate variables
        this.ccOperatingFrom = actorObject.aptmap.operatingFrom || undefined;
        this.ccVictims = actorObject.aptmap.victims || undefined;
    }

    public synonymsString(): string {
        return this.synonyms.join(', ');
    }

    public getColorMapping(): any {
        const colors: any = {};
        for (const v of this.ccVictims) {
            colors[v] = {
                fillKey: 'Victim',
            };
        }

        if (this.ccOperatingFrom) {
            colors[this.ccOperatingFrom] = {
                fillKey: 'Threat Actor',
            };
        }
        return colors;
    }
}
