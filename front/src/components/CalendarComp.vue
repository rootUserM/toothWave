<template>
  <div>
    <div
      v-if="showControls"
      class="d-flex flex-colum align-center justify-center"
    >
      <v-btn icon class="ma-2" @click="$refs.calendar.prev()">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <v-select
        :menu-props="{ buttom: true, offsetY: true }"
        v-model="type"
        :items="types"
        dense
        outlined
        hide-details
        class="ma-2"
        label="Tipo de visión"
      ></v-select>
      <v-spacer></v-spacer>
      <v-btn icon class="ma-2" @click="$refs.calendar.next()">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </div>
    <v-calendar
      ref="calendar"
      v-model="value"
      :weekdays="weekday"
      :type="type"
      :first-interval="9"
      :events="comp_events"
      :event-overlap-mode="mode"
      :event-overlap-threshold="30"
      :event-color="getEventColor"
      @change="getEvents"
      @click:event="showAppointment"
    ></v-calendar>
    <v-menu
      v-model="selectedOpen"
      :close-on-content-click="false"
      :activator="selectedElement"
      offset-x
    >
      <v-card color="grey lighten-4" min-width="350px" flat>
        <v-toolbar :color="selectedEvent.color" dark>
          <v-btn icon>
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-toolbar-title> Detalle de Cita </v-toolbar-title>
          <v-spacer></v-spacer>

          <v-btn icon>
            <v-icon>mdi-dots-vertical</v-icon>
            <!-- Agregar acciones como: editar , enviar recordatorio  -->
          </v-btn>
        </v-toolbar>
        <v-card-text>
          <!-- <span v-html="selectedEvent.details"></span> -->
          <v-col>
            <v-simple-table dense>
              <tbody v-if="selectedEvent.patient">
                <!-- <tr>
                        <td width="200px"><b>Consultorio</b></td>
                        <td>{{this.consulting_room.data.name}}</td>
                    </tr> -->
                <tr>
                  <td width="200px"><b>Motivo de visita</b></td>
                  <td>{{ selectedEvent.patient.appointmentMotive }}</td>
                </tr>
                <tr>
                  <td width="200px"><b>Fecha agenda</b></td>
                  <td>
                    {{ selectedEvent.patient.appointmentDate }}
                    {{ selectedEvent.patient.appointmentHour }}
                  </td>
                </tr>
                <tr>
                  <td width="200px"><b>Estatus de cita</b></td>
                  <td>Programada</td>
                </tr>
                <tr>
                  <td width="200px"><b>Paciente</b></td>
                  <td>
                    {{ selectedEvent.patient.patient_info.Name }}
                    {{ selectedEvent.patient.patient_info.Last_name }}
                  </td>
                </tr>
                <tr>
                  <td width="200px"><b>No. De Px</b></td>
                  <td>{{ selectedEvent.patient.patient_info.id }}</td>
                </tr>
                <tr>
                  <td width="200px"><b>Número Telefónico</b></td>
                  <td>
                    {{ selectedEvent.patient.patient_info.PhoneNumber }} |
                    Enviar mensaje
                    <v-btn
                      icon
                      :href="`https://api.whatsapp.com/send?phone=${selectedEvent.patient.patient_info.PhoneNumber}`"
                      target="_blanck"
                    >
                      <!-- Enviar recordatorio -->
                      <v-icon>mdi-whatsapp</v-icon>
                      <!-- Agregar acciones como: editar , enviar recordatorio  -->
                    </v-btn>
                  </td>
                </tr>
                <tr>
                  <td width="200px"><b>Correo</b></td>
                  <td>{{ selectedEvent.patient.patient_info.Email }}</td>
                </tr>
              </tbody>
            </v-simple-table>
          </v-col>
        </v-card-text>
        <v-card-actions>
          <v-btn
            text
            color="secondary"
            @click="selectedOpen = false"
            class="text-none"
          >
            Cancel
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-menu>
  </div>
</template>
<script>
export default {
  name: "CalendarComp",
  props: {
    events: Array,
    calendarshow: String,
    showControls: Boolean,
  },
  mounted() {
    if (this.calendarshow) {
      this.type = this.calendarshow;
    }
  },
  data: () => ({
    type: "month",
    types: [
      { text: "Por mes", value: "month" },
      { text: "Por semana", value: "week" },
      { text: "Por día", value: "day" },
    ],
    mode: "stack",
    modes: ["stack", "column"],
    weekday: [1, 2, 3, 4, 5, 6],
    weekdays: [
      { text: "Sun - Sat", value: [0, 1, 2, 3, 4, 5, 6] },
      { text: "Mon - Sun", value: [1, 2, 3, 4, 5, 6, 0] },
      { text: "Mon - Fri", value: [1, 2, 3, 4, 5] },
      { text: "Mon, Wed, Fri", value: [1, 3, 5] },
    ],
    value: "",
    comp_events: [],
    colors: [
      "blue",
      "indigo",
      "deep-purple",
      "cyan",
      "green",
      "orange",
      "grey yellow",
    ],
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
  }),
  methods: {
    showAppointment({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event;
        this.selectedElement = nativeEvent.target;
        requestAnimationFrame(() =>
          requestAnimationFrame(() => (this.selectedOpen = true))
        );
      };

      if (this.selectedOpen) {
        this.selectedOpen = false;
        requestAnimationFrame(() => requestAnimationFrame(() => open()));
      } else {
        open();
      }

      nativeEvent.stopPropagation();
    },
    getEvents() {
      const local_events = [];

      for (let i = 0; i < this.events.length; i++) {
        var date_min =
          this.events[i].appointmentDate + "T" + this.events[i].appointmentHour;
        const min = new Date(date_min);
        const max = new Date(min.getTime() + 60 * 60 * 1000);
        const firstTimestamp = min.getTime();
        const first = new Date(firstTimestamp - (firstTimestamp % 900000));
        const secondTimestamp = max.getTime();
        const second = new Date(secondTimestamp - (secondTimestamp % 900000));
        local_events.push({
          name: this.events[i].appointmentMotive,
          start: first,
          end: second,
          color: this.colors[this.rnd(0, this.colors.length - 1)],
          timed: true,
          patient: this.events[i],
        });
      }
      this.comp_events = local_events;
    },
    getEventColor(event) {
      return event.color;
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a;
    },
  },
};
</script>
<style scoped>
.v-calendar-daily {
  height: 500px !important;
}
</style>
